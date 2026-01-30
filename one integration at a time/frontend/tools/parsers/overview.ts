/**
 * Overview Parser Plugin
 * Orchestr8 v3.0 - The Fortress Factory
 * 
 * Scans a project directory and generates a numbered index overview.
 * This plugin provides a high-level view of the project structure.
 * 
 * Usage:
 *   npx tsx scaffold-cli.ts overview --target ./my-project
 *   npx tsx scaffold-cli.ts overview --target ./my-project --filter "*.ts"
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { ScaffoldPlugin, ParserOptions } from '../scaffold-cli.js';

// Directory patterns to ignore
const IGNORE_PATTERNS = [
    'node_modules',
    '.git',
    '__pycache__',
    '.venv',
    'venv',
    'dist',
    'build',
    '.next',
    '.nuxt',
    'coverage',
    '.pytest_cache',
    '.mypy_cache',
    '.tox',
    'eggs',
    '*.egg-info',
    '.DS_Store'
];

/**
 * File entry in the overview index.
 */
interface FileEntry {
    index: number;
    path: string;
    name: string;
    type: 'file' | 'directory';
    size?: number;
    extension?: string;
}

/**
 * Overview result structure.
 */
interface OverviewResult {
    projectPath: string;
    totalFiles: number;
    totalDirectories: number;
    entries: FileEntry[];
    timestamp: string;
}

/**
 * Check if a path should be ignored based on patterns.
 */
function shouldIgnore(name: string): boolean {
    return IGNORE_PATTERNS.some(pattern => {
        if (pattern.includes('*')) {
            const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
            return regex.test(name);
        }
        return name === pattern;
    });
}

/**
 * Check if a file matches the filter pattern.
 */
function matchesFilter(name: string, filter?: string): boolean {
    if (!filter) return true;
    
    // Support glob-like patterns
    if (filter.includes('*')) {
        const regex = new RegExp('^' + filter.replace(/\./g, '\\.').replace(/\*/g, '.*') + '$');
        return regex.test(name);
    }
    
    // Simple substring match
    return name.includes(filter);
}

/**
 * Recursively scan directory and build file index.
 */
async function scanDirectory(
    dirPath: string,
    basePath: string,
    filter?: string,
    entries: FileEntry[] = [],
    indexCounter = { value: 1 }
): Promise<void> {
    try {
        const items = await fs.readdir(dirPath, { withFileTypes: true });
        
        // Sort: directories first, then files, alphabetically
        items.sort((a, b) => {
            if (a.isDirectory() && !b.isDirectory()) return -1;
            if (!a.isDirectory() && b.isDirectory()) return 1;
            return a.name.localeCompare(b.name);
        });
        
        for (const item of items) {
            if (shouldIgnore(item.name)) continue;
            
            const fullPath = path.join(dirPath, item.name);
            const relativePath = path.relative(basePath, fullPath);
            
            if (item.isDirectory()) {
                // Add directory entry
                entries.push({
                    index: indexCounter.value++,
                    path: relativePath,
                    name: item.name,
                    type: 'directory'
                });
                
                // Recursively scan subdirectory
                await scanDirectory(fullPath, basePath, filter, entries, indexCounter);
            } else {
                // Check filter
                if (!matchesFilter(item.name, filter)) continue;
                
                // Get file stats
                const stats = await fs.stat(fullPath);
                const extension = path.extname(item.name).slice(1) || undefined;
                
                entries.push({
                    index: indexCounter.value++,
                    path: relativePath,
                    name: item.name,
                    type: 'file',
                    size: stats.size,
                    extension
                });
            }
        }
    } catch (err) {
        console.error(`Error scanning ${dirPath}:`, err);
    }
}

/**
 * Format file size for display.
 */
function formatSize(bytes?: number): string {
    if (bytes === undefined) return '';
    if (bytes < 1024) return `${bytes}B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
}

/**
 * Generate text report from overview result.
 */
function generateReport(result: OverviewResult): string {
    const lines: string[] = [
        `# Project Overview`,
        ``,
        `**Path:** ${result.projectPath}`,
        `**Generated:** ${result.timestamp}`,
        `**Files:** ${result.totalFiles} | **Directories:** ${result.totalDirectories}`,
        ``,
        `## Index`,
        ``
    ];
    
    for (const entry of result.entries) {
        const indent = '  '.repeat(entry.path.split(path.sep).length - 1);
        const icon = entry.type === 'directory' ? '📁' : '📄';
        const size = entry.type === 'file' ? ` (${formatSize(entry.size)})` : '';
        
        lines.push(`${String(entry.index).padStart(4)}. ${indent}${icon} ${entry.name}${size}`);
    }
    
    return lines.join('\n');
}

/**
 * Main parser function - scans project and returns numbered index.
 */
async function parseOverview(targetPath: string, options: ParserOptions): Promise<string | OverviewResult> {
    const absolutePath = path.resolve(targetPath);
    
    // Verify target exists
    try {
        await fs.access(absolutePath);
    } catch {
        throw new Error(`Target path does not exist: ${absolutePath}`);
    }
    
    const entries: FileEntry[] = [];
    await scanDirectory(absolutePath, absolutePath, options.filter, entries);
    
    const result: OverviewResult = {
        projectPath: absolutePath,
        totalFiles: entries.filter(e => e.type === 'file').length,
        totalDirectories: entries.filter(e => e.type === 'directory').length,
        entries,
        timestamp: new Date().toISOString()
    };
    
    // Return text report for CLI, or JSON if requested
    if (options.json) {
        return result;
    }
    
    return generateReport(result);
}

/**
 * Overview Plugin Implementation
 */
const plugin: ScaffoldPlugin = {
    commandType: 'overview',
    description: 'Generate a numbered index overview of the project structure',
    parserFunction: parseOverview,
    supportsCompare: false,
    specificOptions: {
        json: {
            type: 'boolean',
            description: 'Output as JSON instead of text report',
            default: false
        }
    }
};

export default plugin;
