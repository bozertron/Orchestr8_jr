#!/usr/bin/env node
/**
 * Scaffold CLI - TypeScript Plugin Protocol
 * Orchestr8 v3.0 - The Fortress Factory
 * 
 * A CLI tool for discovering and executing TypeScript parser plugins.
 * Designed to be called from Python via subprocess.
 * 
 * Requirements:
 *   - Node.js 22+
 *   - tsx (npm install -g tsx)
 *   - commander (npm install commander)
 * 
 * Usage:
 *   npx tsx scaffold-cli.ts list-plugins
 *   npx tsx scaffold-cli.ts <commandType> --target <path> [options]
 * 
 * @module scaffold-cli
 * @version 1.0.0
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { Command, Option } from 'commander';

// ============================================================================
// INTERFACES - The Protocol Contract
// ============================================================================

/**
 * Options passed to parser functions.
 * Contains common options plus any plugin-specific options.
 */
export interface ParserOptions {
    /** Path to compare against (for diff analysis) */
    comparePath?: string;
    /** Filter pattern for narrowing results */
    filter?: string;
    /** UI pattern to search for */
    uiPattern?: string;
    /** File indices (comma-separated) */
    indices?: string;
    /** File paths (comma-separated) */
    paths?: string;
    /** Target directory for analysis */
    target: string;
    /** Allow arbitrary additional options */
    [key: string]: any;
}

/**
 * Plugin-specific option configuration.
 */
export interface PluginOptionConfig {
    /** Short alias for the option (e.g., 'f' for --filter) */
    alias?: string;
    /** Option type */
    type: 'string' | 'boolean' | 'number';
    /** Description for help text */
    description: string;
    /** Default value */
    default?: any;
}

/**
 * ScaffoldPlugin Interface - The Protocol
 * 
 * Every parser plugin must implement this interface to be discoverable
 * and executable by the scaffold-cli.
 */
export interface ScaffoldPlugin {
    /** Unique command identifier (e.g., 'overview', 'stores') */
    commandType: string;
    
    /** Short description for CLI help */
    description: string;
    
    /** 
     * Main parser function
     * @param targetPath - Directory to analyze
     * @param options - Parser options
     * @returns Promise resolving to report string or structured data
     */
    parserFunction: (targetPath: string, options: ParserOptions) => Promise<string | any>;
    
    /** Whether this parser supports --compare-path option */
    supportsCompare: boolean;
    
    /** Plugin-specific options beyond common ones */
    specificOptions?: {
        [key: string]: PluginOptionConfig;
    };
}

/**
 * Plugin metadata returned by list-plugins command.
 */
export interface PluginInfo {
    commandType: string;
    description: string;
    supportsCompare: boolean;
    specificOptions: string[];
}

// ============================================================================
// TYPE GUARD
// ============================================================================

/**
 * Type guard to validate if an object implements ScaffoldPlugin interface.
 * @param obj - Object to validate
 * @returns True if object is a valid ScaffoldPlugin
 */
export function isScaffoldPlugin(obj: any): obj is ScaffoldPlugin {
    return obj &&
        typeof obj.commandType === 'string' &&
        typeof obj.description === 'string' &&
        typeof obj.parserFunction === 'function' &&
        typeof obj.supportsCompare === 'boolean';
}

// ============================================================================
// CONSTANTS
// ============================================================================

const SCRIPT_DIR = path.dirname(new URL(import.meta.url).pathname);
const PARSERS_DIR = path.join(SCRIPT_DIR, 'parsers');
const VERSION = '1.0.0';

// Initialize Commander program
const program = new Command();

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Configure Commander program.
 */
function setupProgram(): void {
    program
        .name('scaffold-cli')
        .description('Orchestr8 v3.0 - TypeScript Plugin Protocol CLI')
        .version(VERSION, '-v, --version', 'Display version number');
}

/**
 * Scan parsers directory and load valid plugins.
 * @returns Array of loaded plugin metadata
 */
async function scanPlugins(): Promise<PluginInfo[]> {
    const plugins: PluginInfo[] = [];
    
    try {
        // Ensure parsers directory exists
        try {
            await fs.access(PARSERS_DIR);
        } catch {
            // Directory doesn't exist, return empty array
            return [];
        }
        
        const files = await fs.readdir(PARSERS_DIR);
        const pluginFiles = files.filter(f => f.endsWith('.js') || f.endsWith('.ts'));
        
        for (const file of pluginFiles) {
            const filePath = path.join(PARSERS_DIR, file);
            
            try {
                // Dynamic import for ESM compatibility
                const pluginModule = await import(filePath);
                const plugin = pluginModule.default || pluginModule;
                
                if (isScaffoldPlugin(plugin)) {
                    plugins.push({
                        commandType: plugin.commandType,
                        description: plugin.description,
                        supportsCompare: plugin.supportsCompare,
                        specificOptions: plugin.specificOptions 
                            ? Object.keys(plugin.specificOptions) 
                            : []
                    });
                }
            } catch (err) {
                // Skip invalid plugin files silently
                console.error(`Warning: Could not load plugin ${file}:`, err);
            }
        }
    } catch (err) {
        console.error('Error scanning plugins directory:', err);
    }
    
    return plugins;
}

/**
 * Execute list-plugins command.
 * Outputs JSON array of discovered plugins.
 * Supports silent/machine mode for clean JSON output.
 * @param jsonMode - Force JSON output mode (no human-readable messages)
 */
async function listPlugins(jsonMode: boolean = false): Promise<void> {
    // Detect machine mode: non-TTY or explicit --json flag
    const isMachineMode = jsonMode || !process.stdout.isTTY;
    
    // Human-readable header only in interactive mode
    if (!isMachineMode) {
        console.log('Listing available plugins...');
    }
    
    const plugins = await scanPlugins();
    
    // Compact JSON in machine mode, pretty-printed in human mode
    const indent = isMachineMode ? 0 : 2;
    console.log(JSON.stringify(plugins, null, indent));
}

/**
 * Register the list-plugins command with Commander.
 * Supports --json flag for machine-readable output.
 */
function registerListPluginsCommand(): void {
    program
        .command('list-plugins')
        .description('List available parser plugins as JSON')
        .option('--json', 'Output clean JSON without human-readable messages')
        .action(async (options) => {
            await listPlugins(options.json || false);
        });
}

/**
 * Execute a specific plugin.
 * @param commandType - Plugin command to execute
 * @param options - Parser options
 */
async function executePlugin(commandType: string, options: ParserOptions): Promise<void> {
    // Try both .ts and .js extensions
    const extensions = ['.ts', '.js'];
    let pluginPath: string | null = null;
    
    for (const ext of extensions) {
        const testPath = path.join(PARSERS_DIR, `${commandType}${ext}`);
        try {
            await fs.access(testPath);
            pluginPath = testPath;
            break;
        } catch {
            continue;
        }
    }
    
    if (!pluginPath) {
        const plugins = await scanPlugins();
        console.error(`Error: Plugin '${commandType}' not found.`);
        console.error('Available plugins:', plugins.map(p => p.commandType).join(', ') || 'none');
        process.exit(1);
    }
    
    try {
        const pluginModule = await import(pluginPath);
        const loadedPlugin = pluginModule.default || pluginModule;
        
        if (!isScaffoldPlugin(loadedPlugin)) {
            throw new Error('Invalid plugin structure - must implement ScaffoldPlugin interface');
        }
        
        const result = await loadedPlugin.parserFunction(options.target, options);
        
        if (typeof result === 'string') {
            console.log(result);
        } else {
            console.log(JSON.stringify(result, null, 2));
        }
    } catch (err) {
        console.error(`Error executing plugin '${commandType}':`, err);
        process.exit(1);
    }
}

/**
 * Register dynamic plugin commands with Commander.
 * Scans available plugins and creates commands for each.
 */
async function registerPluginCommands(): Promise<void> {
    const plugins = await scanPlugins();
    
    for (const plugin of plugins) {
        const cmd = program
            .command(plugin.commandType)
            .description(plugin.description)
            .option('-t, --target <path>', 'Target directory to analyze', '.')
            .option('-c, --compare-path <path>', 'Compare with another version')
            .option('-f, --filter <pattern>', 'Filter results by pattern')
            .option('-o, --output-dir <path>', 'Output directory for reports');
        
        // Add plugin-specific options
        for (const optName of plugin.specificOptions) {
            cmd.option(`--${optName} <value>`, `Plugin-specific: ${optName}`);
        }
        
        cmd.action(async (cmdOptions) => {
            const options: ParserOptions = {
                target: cmdOptions.target || '.',
                comparePath: cmdOptions.comparePath,
                filter: cmdOptions.filter,
                ...cmdOptions
            };
            await executePlugin(plugin.commandType, options);
        });
    }
}

/**
 * Handle unknown commands by attempting plugin execution.
 * This allows plugins to be called even if not pre-registered.
 */
function setupUnknownCommandHandler(): void {
    program.on('command:*', async (operands) => {
        const commandType = operands[0];
        const args = process.argv.slice(3);
        
        // Parse remaining args into options
        const options: ParserOptions = { target: '.' };
        for (let i = 0; i < args.length; i++) {
            const arg = args[i];
            if (arg.startsWith('--')) {
                const key = arg.slice(2);
                const nextArg = args[i + 1];
                if (nextArg && !nextArg.startsWith('--')) {
                    options[key] = nextArg;
                    i++;
                } else {
                    options[key] = true;
                }
            }
        }
        
        await executePlugin(commandType, options);
    });
}

// ============================================================================
// MAIN ENTRY POINT
// ============================================================================

async function main(): Promise<void> {
    // Setup Commander program
    setupProgram();
    
    // Register built-in commands
    registerListPluginsCommand();
    
    // Register discovered plugin commands
    await registerPluginCommands();
    
    // Handle unknown commands (try as plugin)
    setupUnknownCommandHandler();
    
    // Parse command line arguments
    await program.parseAsync(process.argv);
}

// Run main function
main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
