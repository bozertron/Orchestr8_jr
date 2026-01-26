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

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Display help message.
 */
function showHelp(): void {
    console.log(`
Scaffold CLI v${VERSION}
Orchestr8 v3.0 - The Fortress Factory

Usage:
  npx tsx scaffold-cli.ts <command> [options]

Commands:
  list-plugins              List available parser plugins
  <commandType>             Run a specific parser plugin

Common Options:
  --target <path>           Target directory to analyze (default: .)
  --compare-path <path>     Compare with another version
  --filter <pattern>        Filter results by pattern
  --output-dir <path>       Output directory for reports
  --help, -h                Show this help message
  --version, -v             Show version number

Examples:
  npx tsx scaffold-cli.ts list-plugins
  npx tsx scaffold-cli.ts overview --target ./my-project
  npx tsx scaffold-cli.ts stores --target ./my-project --filter "user"

For plugin-specific options, run:
  npx tsx scaffold-cli.ts <commandType> --help
`);
}

/**
 * Display version.
 */
function showVersion(): void {
    console.log(`scaffold-cli v${VERSION}`);
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
 */
async function listPlugins(): Promise<void> {
    const plugins = await scanPlugins();
    
    if (plugins.length === 0) {
        console.log(JSON.stringify([], null, 2));
        return;
    }
    
    console.log(JSON.stringify(plugins, null, 2));
}

/**
 * Execute a specific plugin.
 * @param commandType - Plugin command to execute
 * @param options - Parser options
 */
async function executePlugin(commandType: string, options: ParserOptions): Promise<void> {
    const plugins = await scanPlugins();
    const plugin = plugins.find(p => p.commandType === commandType);
    
    if (!plugin) {
        console.error(`Error: Plugin '${commandType}' not found.`);
        console.error('Available plugins:', plugins.map(p => p.commandType).join(', ') || 'none');
        process.exit(1);
    }
    
    // Load and execute the plugin
    const pluginPath = path.join(PARSERS_DIR, `${commandType}.js`);
    
    try {
        const pluginModule = await import(pluginPath);
        const loadedPlugin = pluginModule.default || pluginModule;
        
        if (!isScaffoldPlugin(loadedPlugin)) {
            throw new Error('Invalid plugin structure');
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
 * Parse command line arguments.
 * @param args - Command line arguments
 * @returns Parsed options
 */
function parseArgs(args: string[]): { command: string; options: ParserOptions } {
    const options: ParserOptions = {
        target: '.'
    };
    
    let command = '';
    
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        
        if (arg === '--help' || arg === '-h') {
            showHelp();
            process.exit(0);
        }
        
        if (arg === '--version' || arg === '-v') {
            showVersion();
            process.exit(0);
        }
        
        if (arg.startsWith('--')) {
            const key = arg.slice(2);
            const nextArg = args[i + 1];
            
            if (nextArg && !nextArg.startsWith('--')) {
                options[key] = nextArg;
                i++;
            } else {
                options[key] = true;
            }
        } else if (!arg.startsWith('-') && !command) {
            command = arg;
        }
    }
    
    return { command, options };
}

// ============================================================================
// MAIN ENTRY POINT
// ============================================================================

async function main(): Promise<void> {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        showHelp();
        process.exit(0);
    }
    
    const { command, options } = parseArgs(args);
    
    if (command === 'list-plugins') {
        await listPlugins();
    } else if (command) {
        await executePlugin(command, options);
    } else {
        showHelp();
        process.exit(1);
    }
}

// Run main function
main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
