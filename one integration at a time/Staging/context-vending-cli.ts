#!/usr/bin/env node
// context-vending-cli.ts
// The Context Vending Machine CLI - Build task libraries offline, unleash agent swarms later!

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, resolve } from 'path';
import * as readline from 'readline';
import { createHash } from 'crypto';

interface Task {
  id: string;
  created: string;
  type: 'bug' | 'feature' | 'refactor' | 'optimization';
  priority: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  context: {
    files: string[];
    patterns: string[];
    dependencies: string[];
    testFiles: string[];
  };
  enhancedPrompt: string;
  status: 'pending' | 'in-progress' | 'completed';
  agentNotes?: string;
}

interface TaskLibrary {
  name: string;
  created: string;
  lastModified: string;
  tasks: Task[];
  projectMetadata: {
    rootPath: string;
    primaryLanguages: string[];
    frameworks: string[];
  };
}

class ContextVendingCLI {
  private rl: readline.Interface;
  private currentLibrary: TaskLibrary | null = null;
  private libraryPath: string;
  private projectRoot: string;

  constructor() {
    this.projectRoot = process.cwd();
    this.libraryPath = join(this.projectRoot, '.context-vending-library');
    
    // Ensure library directory exists
    if (!existsSync(this.libraryPath)) {
      mkdirSync(this.libraryPath, { recursive: true });
    }

    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }

  async start() {
    console.clear();
    console.log(`
╔══════════════════════════════════════════════════════════════════╗
║          🎰 CONTEXT VENDING MACHINE - CLI EDITION 🎰             ║
║                                                                  ║
║   Build context-rich task libraries offline, then unleash       ║
║   your agent swarm with perfect context when ready!             ║
╚══════════════════════════════════════════════════════════════════╝
`);

    await this.mainMenu();
  }

  private async mainMenu() {
    const choice = await this.prompt(`
📚 Main Menu:
1) Create New Task Library
2) Load Existing Library
3) Quick Task Entry
4) Export for Agent Swarm
5) View Statistics
6) Exit

Choose [1-6]: `);

    switch (choice) {
      case '1':
        await this.createNewLibrary();
        break;
      case '2':
        await this.loadLibrary();
        break;
      case '3':
        await this.quickTaskEntry();
        break;
      case '4':
        await this.exportForAgents();
        break;
      case '5':
        await this.viewStatistics();
        break;
      case '6':
        this.exit();
        break;
      default:
        console.log('Invalid choice. Please try again.');
        await this.mainMenu();
    }
  }

  private async createNewLibrary() {
    const name = await this.prompt('\n📚 Library name: ');
    
    this.currentLibrary = {
      name,
      created: new Date().toISOString(),
      lastModified: new Date().toISOString(),
      tasks: [],
      projectMetadata: {
        rootPath: this.projectRoot,
        primaryLanguages: this.detectLanguages(),
        frameworks: this.detectFrameworks()
      }
    };

    this.saveLibrary();
    console.log(`\n✅ Created library: ${name}`);
    
    await this.libraryMenu();
  }

  private async libraryMenu() {
    if (!this.currentLibrary) {
      console.log('No library loaded!');
      await this.mainMenu();
      return;
    }

    const choice = await this.prompt(`
📖 Library: ${this.currentLibrary.name} (${this.currentLibrary.tasks.length} tasks)

1) Add Task (Structured)
2) Add Task (Natural Language)
3) Bulk Import from File
4) View Tasks
5) Generate Context Map
6) Save & Return

Choose [1-6]: `);

    switch (choice) {
      case '1':
        await this.addStructuredTask();
        break;
      case '2':
        await this.addNaturalLanguageTask();
        break;
      case '3':
        await this.bulkImport();
        break;
      case '4':
        await this.viewTasks();
        break;
      case '5':
        await this.generateContextMap();
        break;
      case '6':
        this.saveLibrary();
        await this.mainMenu();
        return;
    }

    await this.libraryMenu();
  }

  private async addStructuredTask() {
    console.log('\n📝 Structured Task Entry:\n');

    const type = await this.promptWithOptions('Type', ['bug', 'feature', 'refactor', 'optimization']);
    const priority = await this.promptWithOptions('Priority', ['low', 'medium', 'high', 'critical']);
    const title = await this.prompt('Title: ');
    const description = await this.prompt('Description (press Enter twice to finish):\n', true);
    
    // Context gathering
    console.log('\n🎯 Context Definition:');
    const files = await this.promptList('Related files (comma-separated): ');
    const patterns = await this.promptList('Code patterns to consider: ');
    const dependencies = await this.promptList('Dependencies involved: ');
    const testFiles = await this.promptList('Test files to update: ');

    // Auto-generate enhanced prompt
    const enhancedPrompt = this.generateEnhancedPrompt({
      type, title, description,
      context: { files, patterns, dependencies, testFiles }
    });

    const task: Task = {
      id: this.generateId(),
      created: new Date().toISOString(),
      type: type as Task['type'],
      priority: priority as Task['priority'],
      title,
      description,
      context: {
        files: this.expandFilePaths(files),
        patterns,
        dependencies,
        testFiles: this.expandFilePaths(testFiles)
      },
      enhancedPrompt,
      status: 'pending'
    };

    this.currentLibrary!.tasks.push(task);
    console.log(`\n✅ Task added: ${task.id}`);
    
    // Show preview
    console.log('\n📋 Enhanced Prompt Preview:');
    console.log(enhancedPrompt.substring(0, 500) + '...\n');
  }

  private async addNaturalLanguageTask() {
    console.log('\n💬 Natural Language Task Entry:\n');
    console.log('Describe your task in natural language. I\'ll extract the context!\n');

    const input = await this.prompt('Task description (press Enter twice to finish):\n', true);
    
    // Parse natural language
    const parsed = this.parseNaturalLanguage(input);
    
    console.log('\n🔍 Extracted Context:');
    console.log(`Type: ${parsed.type}`);
    console.log(`Priority: ${parsed.priority}`);
    console.log(`Files: ${parsed.files.join(', ')}`);
    console.log(`Patterns: ${parsed.patterns.join(', ')}`);

    const confirm = await this.prompt('\nAccept extracted context? [Y/n]: ');
    if (confirm.toLowerCase() === 'n') {
      // Allow manual editing
      parsed.type = await this.promptWithOptions('Type', ['bug', 'feature', 'refactor', 'optimization']) as any;
      parsed.priority = await this.promptWithOptions('Priority', ['low', 'medium', 'high', 'critical']) as any;
    }

    const task: Task = {
      id: this.generateId(),
      created: new Date().toISOString(),
      type: parsed.type,
      priority: parsed.priority,
      title: parsed.title,
      description: input,
      context: {
        files: this.expandFilePaths(parsed.files),
        patterns: parsed.patterns,
        dependencies: parsed.dependencies,
        testFiles: parsed.testFiles
      },
      enhancedPrompt: this.generateEnhancedPrompt({
        type: parsed.type,
        title: parsed.title,
        description: input,
        context: {
          files: parsed.files,
          patterns: parsed.patterns,
          dependencies: parsed.dependencies,
          testFiles: parsed.testFiles
        }
      }),
      status: 'pending'
    };

    this.currentLibrary!.tasks.push(task);
    console.log(`\n✅ Task added: ${task.id}`);
  }

  private parseNaturalLanguage(input: string): any {
    // Smart pattern matching for natural language parsing
    const result = {
      type: 'feature' as Task['type'],
      priority: 'medium' as Task['priority'],
      title: '',
      files: [] as string[],
      patterns: [] as string[],
      dependencies: [] as string[],
      testFiles: [] as string[]
    };

    // Type detection
    if (/bug|error|fix|broken|crash/i.test(input)) result.type = 'bug';
    if (/feature|add|implement|create/i.test(input)) result.type = 'feature';
    if (/refactor|clean|improve|reorganize/i.test(input)) result.type = 'refactor';
    if (/optimize|performance|speed|memory/i.test(input)) result.type = 'optimization';

    // Priority detection
    if (/critical|urgent|asap|blocker/i.test(input)) result.priority = 'critical';
    if (/high|important/i.test(input)) result.priority = 'high';
    if (/low|minor|nice.to.have/i.test(input)) result.priority = 'low';

    // Extract title (first line or first sentence)
    const firstLine = input.split('\n')[0];
    result.title = firstLine.length > 60 ? firstLine.substring(0, 60) + '...' : firstLine;

    // File extraction
    const fileRegex = /(?:in |at |file |component )?([\w\-\/]+\.(vue|ts|rs|js))/g;
    let match;
    while ((match = fileRegex.exec(input)) !== null) {
      result.files.push(match[1]);
    }

    // Pattern extraction
    if (/invoke|tauri command/i.test(input)) result.patterns.push('Tauri command pattern');
    if (/reactive|ref|computed/i.test(input)) result.patterns.push('Vue reactivity pattern');
    if (/async|await|promise/i.test(input)) result.patterns.push('Async pattern');

    return result;
  }

  private generateEnhancedPrompt(taskData: any): string {
    return `## 🎯 Task: ${taskData.title}

**Type**: ${taskData.type.toUpperCase()}
**Priority**: ${taskData.priority.toUpperCase()}

### 📋 Description:
${taskData.description}

### 📍 Context Files:
${taskData.context.files.map((f: string) => `- ${f}`).join('\n')}

### 🔍 Patterns to Consider:
${taskData.context.patterns.map((p: string) => `- ${p}`).join('\n')}

### 📦 Dependencies:
${taskData.context.dependencies.map((d: string) => `- ${d}`).join('\n')}

### 🧪 Test Files:
${taskData.context.testFiles.map((t: string) => `- ${t}`).join('\n')}

### 🎯 Implementation Request:
Please implement this ${taskData.type} following the established patterns in the codebase. Ensure all changes maintain consistency with the existing architecture and update any affected test files.`;
  }

  private async exportForAgents() {
    const libraries = this.listLibraries();
    if (libraries.length === 0) {
      console.log('\nNo libraries found!');
      await this.mainMenu();
      return;
    }

    console.log('\n📚 Available Libraries:');
    libraries.forEach((lib, i) => {
      const data = JSON.parse(readFileSync(join(this.libraryPath, lib), 'utf-8'));
      console.log(`${i + 1}) ${data.name} (${data.tasks.length} tasks)`);
    });

    const choice = await this.prompt('\nSelect library to export [number]: ');
    const libIndex = parseInt(choice) - 1;

    if (libIndex >= 0 && libIndex < libraries.length) {
      const libData = JSON.parse(readFileSync(join(this.libraryPath, libraries[libIndex]), 'utf-8'));
      
      // Generate agent-ready format
      const agentFormat = {
        version: '1.0',
        generated: new Date().toISOString(),
        library: libData.name,
        projectContext: libData.projectMetadata,
        taskQueue: libData.tasks.filter((t: Task) => t.status === 'pending').map((task: Task) => ({
          id: task.id,
          priority: task.priority,
          enhancedPrompt: task.enhancedPrompt,
          context: task.context
        }))
      };

      const exportPath = join(this.projectRoot, `agent-tasks-${Date.now()}.json`);
      writeFileSync(exportPath, JSON.stringify(agentFormat, null, 2));
      
      console.log(`\n✅ Exported ${agentFormat.taskQueue.length} tasks to: ${exportPath}`);
      console.log('\n🤖 Ready for agent consumption!');
    }

    await this.mainMenu();
  }

  private async viewTasks() {
    if (!this.currentLibrary || this.currentLibrary.tasks.length === 0) {
      console.log('\nNo tasks in library!');
      return;
    }

    console.log(`\n📋 Tasks in ${this.currentLibrary.name}:\n`);
    
    this.currentLibrary.tasks.forEach((task, i) => {
      console.log(`${i + 1}) [${task.priority.toUpperCase()}] ${task.type}: ${task.title}`);
      console.log(`   Status: ${task.status} | Files: ${task.context.files.length} | ID: ${task.id}`);
      console.log('');
    });

    const choice = await this.prompt('View task details [number] or [Enter] to return: ');
    if (choice) {
      const index = parseInt(choice) - 1;
      if (index >= 0 && index < this.currentLibrary.tasks.length) {
        const task = this.currentLibrary.tasks[index];
        console.log('\n' + '='.repeat(70));
        console.log(task.enhancedPrompt);
        console.log('='.repeat(70) + '\n');
        
        await this.prompt('Press Enter to continue...');
      }
    }
  }

  // Helper methods
  private async prompt(question: string, multiline = false): Promise<string> {
    if (multiline) {
      console.log(question);
      const lines: string[] = [];
      
      return new Promise((resolve) => {
        const captureLines = () => {
          this.rl.question('', (line) => {
            if (line === '') {
              resolve(lines.join('\n'));
            } else {
              lines.push(line);
              captureLines();
            }
          });
        };
        captureLines();
      });
    }

    return new Promise((resolve) => {
      this.rl.question(question, resolve);
    });
  }

  private async promptWithOptions(label: string, options: string[]): Promise<string> {
    console.log(`\n${label}:`);
    options.forEach((opt, i) => console.log(`  ${i + 1}) ${opt}`));
    const choice = await this.prompt('Choose [number]: ');
    const index = parseInt(choice) - 1;
    return options[index] || options[0];
  }

  private async promptList(question: string): Promise<string[]> {
    const input = await this.prompt(question);
    return input.split(',').map(s => s.trim()).filter(s => s);
  }

  private expandFilePaths(files: string[]): string[] {
    // Expand relative paths and verify existence
    return files.map(file => {
      const fullPath = resolve(this.projectRoot, file);
      if (existsSync(fullPath)) {
        return file;
      }
      // Try common locations
      const commonPaths = [
        join('frontend/src/components', file),
        join('src-tauri/src', file),
        join('src', file)
      ];
      
      for (const commonPath of commonPaths) {
        if (existsSync(join(this.projectRoot, commonPath))) {
          return commonPath;
        }
      }
      
      return file; // Return as-is if not found
    });
  }

  private detectLanguages(): string[] {
    const languages: Set<string> = new Set();
    
    if (existsSync(join(this.projectRoot, 'package.json'))) languages.add('JavaScript/TypeScript');
    if (existsSync(join(this.projectRoot, 'Cargo.toml'))) languages.add('Rust');
    if (existsSync(join(this.projectRoot, 'go.mod'))) languages.add('Go');
    if (existsSync(join(this.projectRoot, 'pyproject.toml'))) languages.add('Python');
    
    return Array.from(languages);
  }

  private detectFrameworks(): string[] {
    const frameworks: Set<string> = new Set();
    
    try {
      const packageJson = JSON.parse(readFileSync(join(this.projectRoot, 'package.json'), 'utf-8'));
      const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
      
      if (deps.vue) frameworks.add('Vue.js');
      if (deps.react) frameworks.add('React');
      if (deps['@tauri-apps/api']) frameworks.add('Tauri');
      if (deps.vite) frameworks.add('Vite');
    } catch {}
    
    return Array.from(frameworks);
  }

  private generateId(): string {
    return createHash('md5')
      .update(Date.now().toString() + Math.random().toString())
      .digest('hex')
      .substring(0, 8);
  }

  private saveLibrary() {
    if (!this.currentLibrary) return;
    
    this.currentLibrary.lastModified = new Date().toISOString();
    const filename = `${this.currentLibrary.name.replace(/\s+/g, '-').toLowerCase()}.json`;
    const filepath = join(this.libraryPath, filename);
    
    writeFileSync(filepath, JSON.stringify(this.currentLibrary, null, 2));
  }

  private listLibraries(): string[] {
    if (!existsSync(this.libraryPath)) return [];
    
    return readdirSync(this.libraryPath)
      .filter(f => f.endsWith('.json'));
  }

  private async loadLibrary() {
    const libraries = this.listLibraries();
    
    if (libraries.length === 0) {
      console.log('\nNo libraries found!');
      await this.mainMenu();
      return;
    }

    console.log('\n📚 Available Libraries:');
    libraries.forEach((lib, i) => {
      const data = JSON.parse(readFileSync(join(this.libraryPath, lib), 'utf-8'));
      console.log(`${i + 1}) ${data.name} (${data.tasks.length} tasks, modified: ${new Date(data.lastModified).toLocaleDateString()})`);
    });

    const choice = await this.prompt('\nSelect library [number]: ');
    const index = parseInt(choice) - 1;

    if (index >= 0 && index < libraries.length) {
      const data = readFileSync(join(this.libraryPath, libraries[index]), 'utf-8');
      this.currentLibrary = JSON.parse(data);
      console.log(`\n✅ Loaded: ${this.currentLibrary!.name}`);
      await this.libraryMenu();
    } else {
      await this.mainMenu();
    }
  }

  private async quickTaskEntry() {
    console.log('\n⚡ Quick Task Entry (one-liner)\n');
    const input = await this.prompt('Task: ');
    
    if (!input) {
      await this.mainMenu();
      return;
    }

    // Create or load default library
    if (!this.currentLibrary) {
      this.currentLibrary = {
        name: 'Quick Tasks',
        created: new Date().toISOString(),
        lastModified: new Date().toISOString(),
        tasks: [],
        projectMetadata: {
          rootPath: this.projectRoot,
          primaryLanguages: this.detectLanguages(),
          frameworks: this.detectFrameworks()
        }
      };
    }

    const parsed = this.parseNaturalLanguage(input);
    const task: Task = {
      id: this.generateId(),
      created: new Date().toISOString(),
      type: parsed.type,
      priority: parsed.priority,
      title: parsed.title,
      description: input,
      context: {
        files: parsed.files,
        patterns: parsed.patterns,
        dependencies: parsed.dependencies,
        testFiles: parsed.testFiles
      },
      enhancedPrompt: this.generateEnhancedPrompt({
        type: parsed.type,
        title: parsed.title,
        description: input,
        context: {
          files: parsed.files,
          patterns: parsed.patterns,
          dependencies: parsed.dependencies,
          testFiles: parsed.testFiles
        }
      }),
      status: 'pending'
    };

    this.currentLibrary.tasks.push(task);
    this.saveLibrary();
    
    console.log(`✅ Quick task added: ${task.id}`);
    
    const another = await this.prompt('\nAdd another? [Y/n]: ');
    if (another.toLowerCase() !== 'n') {
      await this.quickTaskEntry();
    } else {
      await this.mainMenu();
    }
  }

  private async viewStatistics() {
    const libraries = this.listLibraries();
    let totalTasks = 0;
    let pendingTasks = 0;
    let completedTasks = 0;
    const typeCount: Record<string, number> = {};
    const priorityCount: Record<string, number> = {};

    libraries.forEach(lib => {
      const data = JSON.parse(readFileSync(join(this.libraryPath, lib), 'utf-8'));
      totalTasks += data.tasks.length;
      
      data.tasks.forEach((task: Task) => {
        if (task.status === 'pending') pendingTasks++;
        if (task.status === 'completed') completedTasks++;
        
        typeCount[task.type] = (typeCount[task.type] || 0) + 1;
        priorityCount[task.priority] = (priorityCount[task.priority] || 0) + 1;
      });
    });

    console.log(`
📊 Context Vending Statistics
════════════════════════════════════════

📚 Libraries: ${libraries.length}
📋 Total Tasks: ${totalTasks}
⏳ Pending: ${pendingTasks}
✅ Completed: ${completedTasks}

🎯 By Type:
${Object.entries(typeCount).map(([type, count]) => `   ${type}: ${count}`).join('\n')}

🔥 By Priority:
${Object.entries(priorityCount).map(([priority, count]) => `   ${priority}: ${count}`).join('\n')}
`);

    await this.prompt('\nPress Enter to continue...');
    await this.mainMenu();
  }

  private async bulkImport() {
    console.log('\n📥 Bulk Import from File\n');
    console.log('Expected format: One task per line, or TODO/FIXME comments from code\n');
    
    const filepath = await this.prompt('File path: ');
    
    try {
      const content = readFileSync(filepath, 'utf-8');
      const lines = content.split('\n').filter(line => line.trim());
      
      let imported = 0;
      for (const line of lines) {
        // Skip actual code lines, only process comments or task descriptions
        if (line.includes('TODO') || line.includes('FIXME') || !line.includes(';')) {
          const parsed = this.parseNaturalLanguage(line);
          
          const task: Task = {
            id: this.generateId(),
            created: new Date().toISOString(),
            type: parsed.type,
            priority: line.includes('FIXME') ? 'high' : parsed.priority,
            title: parsed.title,
            description: line,
            context: {
              files: parsed.files,
              patterns: parsed.patterns,
              dependencies: parsed.dependencies,
              testFiles: parsed.testFiles
            },
            enhancedPrompt: this.generateEnhancedPrompt({
              type: parsed.type,
              title: parsed.title,
              description: line,
              context: {
                files: parsed.files,
                patterns: parsed.patterns,
                dependencies: parsed.dependencies,
                testFiles: parsed.testFiles
              }
            }),
            status: 'pending'
          };

          this.currentLibrary!.tasks.push(task);
          imported++;
        }
      }

      console.log(`\n✅ Imported ${imported} tasks from ${filepath}`);
      this.saveLibrary();
      
    } catch (error) {
      console.log(`\n❌ Error reading file: ${error}`);
    }
  }

  private async generateContextMap() {
    if (!this.currentLibrary || this.currentLibrary.tasks.length === 0) {
      console.log('\nNo tasks to map!');
      return;
    }

    console.log('\n🗺️  Generating Context Map...\n');

    // Analyze all tasks to find relationships
    const fileGraph = new Map<string, Set<string>>();
    const patternFrequency = new Map<string, number>();

    this.currentLibrary.tasks.forEach(task => {
      // Build file relationship graph
      task.context.files.forEach(file => {
        if (!fileGraph.has(file)) {
          fileGraph.set(file, new Set());
        }
        task.context.files.forEach(otherFile => {
          if (file !== otherFile) {
            fileGraph.get(file)!.add(otherFile);
          }
        });
      });

      // Count pattern frequency
      task.context.patterns.forEach(pattern => {
        patternFrequency.set(pattern, (patternFrequency.get(pattern) || 0) + 1);
      });
    });

    console.log('📍 File Relationships:');
    Array.from(fileGraph.entries())
      .sort((a, b) => b[1].size - a[1].size)
      .slice(0, 10)
      .forEach(([file, related]) => {
        console.log(`   ${file} → connected to ${related.size} other files`);
      });

    console.log('\n🔍 Pattern Frequency:');
    Array.from(patternFrequency.entries())
      .sort((a, b) => b[1] - a[1])
      .forEach(([pattern, count]) => {
        console.log(`   ${pattern}: ${count} occurrences`);
      });

    await this.prompt('\nPress Enter to continue...');
  }

  private exit() {
    console.log('\n👋 Context Vending Machine shutting down. Happy coding!\n');
    this.rl.close();
    process.exit(0);
  }
}

// Auto-start if run directly
if (require.main === module) {
  const cli = new ContextVendingCLI();
  cli.start().catch(console.error);
}

export { ContextVendingCLI };

// Make it executable
// chmod +x context-vending-cli.ts
// npm install -g tsx
// tsx context-vending-cli.ts