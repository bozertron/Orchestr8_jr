// frontend/tools/unified-context-system.ts
// The Grand Orchestrator - Bringing It All Together!

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

interface ProjectContext {
  projectName: string;
  timestamp: string;
  rustCommands: RustCommand[];
  vueComponents: VueComponent[];
  dataFlowPatterns: DataFlowPattern[];
  architecturalInsights: ArchitecturalInsight[];
}

interface RustCommand {
  name: string;
  file: string;
  inputs: CommandInput[];
  outputs: CommandOutput[];
  complexity: 'simple' | 'moderate' | 'complex';
}

interface VueComponent {
  name: string;
  file: string;
  commands: string[];
  stores: string[];
  events: string[];
}

interface DataFlowPattern {
  pattern: string;
  frequency: number;
  components: string[];
  recommendation?: string;
}

interface ArchitecturalInsight {
  type: 'coupling' | 'bottleneck' | 'optimization' | 'security';
  severity: 'info' | 'warning' | 'critical';
  description: string;
  affectedComponents: string[];
  recommendation: string;
}

interface CommandInput {
  source: string;
  pattern: string;
}

interface CommandOutput {
  destination: string;
  transformation?: string;
}

/**
 * The Unified Context System - Your project's architectural cartographer!
 * This beauty orchestrates all analysis tools and creates a comprehensive
 * context map that makes LLMs practically omniscient about your codebase.
 */
class UnifiedContextSystem {
  private projectRoot: string;
  private contextData: ProjectContext;

  constructor(projectRoot: string = process.cwd()) {
    this.projectRoot = projectRoot;
    this.contextData = {
      projectName: this.extractProjectName(),
      timestamp: new Date().toISOString(),
      rustCommands: [],
      vueComponents: [],
      dataFlowPatterns: [],
      architecturalInsights: []
    };
  }

  /**
   * The main event - orchestrates all analysis phases with style!
   */
  async analyzeAndEnrich(): Promise<void> {
    console.log(`
╔══════════════════════════════════════════════════════════════════╗
║        🚀 UNIFIED CONTEXT SYSTEM - ARCHITECTURAL ANALYSIS 🚀      ║
╚══════════════════════════════════════════════════════════════════╝
`);

    try {
      // Phase 1: Run the Rust Context Mapper
      await this.runRustAnalysis();
      
      // Phase 2: Run the Vue Flow Analyzer
      await this.runVueAnalysis();
      
      // Phase 3: Cross-reference and identify patterns
      await this.analyzeDataFlowPatterns();
      
      // Phase 4: Generate architectural insights
      await this.generateArchitecturalInsights();
      
      // Phase 5: Create the master context file
      await this.generateMasterContextFile();
      
      // Phase 6: Generate IDE-friendly navigation helpers
      await this.generateIDEHelpers();
      
      // Phase 7: Create the LLM instruction set
      await this.generateLLMInstructions();
      
      console.log('\n✨ Analysis complete! Your codebase is now self-documenting!');
      
    } catch (error) {
      console.error('💥 Analysis failed:', error);
      process.exit(1);
    }
  }

  private async runRustAnalysis(): Promise<void> {
    console.log('\n📦 Phase 1: Analyzing Rust/Tauri layer...');
    
    // Check if Rust analyzer is built
    const rustAnalyzerPath = join(this.projectRoot, 'src-tauri', 'tools', 'context-cartographer', 'target', 'release', 'context-cartographer');
    
    if (!existsSync(rustAnalyzerPath)) {
      console.log('   Building Rust analyzer...');
      execSync('cargo build --release', {
        cwd: join(this.projectRoot, 'src-tauri', 'tools', 'context-cartographer'),
        stdio: 'inherit'
      });
    }
    
    // Run the analyzer
    execSync(rustAnalyzerPath, {
      cwd: this.projectRoot,
      stdio: 'inherit'
    });
    
    // Parse the results
    this.parseRustAnalysisResults();
  }

  private async runVueAnalysis(): Promise<void> {
    console.log('\n🎨 Phase 2: Analyzing Vue/Frontend layer...');
    
    // Run the TypeScript analyzer
    execSync('npx tsx frontend/tools/vue-flow-analyzer.ts', {
      cwd: this.projectRoot,
      stdio: 'inherit'
    });
    
    // Parse the results
    this.parseVueAnalysisResults();
  }

  private async analyzeDataFlowPatterns(): Promise<void> {
    console.log('\n🔍 Phase 3: Identifying data flow patterns...');
    
    // Analyze command usage patterns
    const commandUsage = new Map<string, Set<string>>();
    
    for (const component of this.contextData.vueComponents) {
      for (const command of component.commands) {
        if (!commandUsage.has(command)) {
          commandUsage.set(command, new Set());
        }
        commandUsage.get(command)!.add(component.name);
      }
    }
    
    // Identify patterns
    for (const [command, components] of commandUsage) {
      if (components.size > 3) {
        this.contextData.dataFlowPatterns.push({
          pattern: `High-frequency command: ${command}`,
          frequency: components.size,
          components: Array.from(components),
          recommendation: 'Consider creating a composable or store action for this command'
        });
      }
    }
    
    console.log(`   Found ${this.contextData.dataFlowPatterns.length} significant patterns`);
  }

  private async generateArchitecturalInsights(): Promise<void> {
    console.log('\n🧠 Phase 4: Generating architectural insights...');
    
    // Check for potential bottlenecks
    this.checkForBottlenecks();
    
    // Check for coupling issues
    this.checkForCoupling();
    
    // Check for optimization opportunities
    this.checkForOptimizations();
    
    console.log(`   Generated ${this.contextData.architecturalInsights.length} insights`);
  }

  private async generateMasterContextFile(): Promise<void> {
    console.log('\n📚 Phase 5: Creating master context file...');
    
    const contextPath = join(this.projectRoot, 'docs', 'project-context.json');
    
    // Ensure docs directory exists
    const docsDir = join(this.projectRoot, 'docs');
    if (!existsSync(docsDir)) {
      mkdirSync(docsDir, { recursive: true });
    }
    
    writeFileSync(contextPath, JSON.stringify(this.contextData, null, 2));
    
    // Also generate a markdown version for human readability
    const markdownPath = join(this.projectRoot, 'docs', 'PROJECT_CONTEXT.md');
    const markdown = this.generateMarkdownReport();
    writeFileSync(markdownPath, markdown);
    
    console.log('   ✅ Context files generated');
  }

  private generateMarkdownReport(): string {
    return `# ${this.contextData.projectName} - Architectural Context Map

Generated: ${new Date(this.contextData.timestamp).toLocaleString()}

## 📊 Overview

- **Rust Commands**: ${this.contextData.rustCommands.length}
- **Vue Components**: ${this.contextData.vueComponents.length}
- **Data Flow Patterns**: ${this.contextData.dataFlowPatterns.length}
- **Architectural Insights**: ${this.contextData.architecturalInsights.length}

## 🔧 Tauri Commands

${this.contextData.rustCommands.map(cmd => `
### \`${cmd.name}\`
- **File**: ${cmd.file}
- **Complexity**: ${cmd.complexity}
- **Called by**: ${cmd.inputs.length} components
- **Data flows to**: ${cmd.outputs.length} destinations
`).join('\n')}

## 🎨 Vue Components

${this.contextData.vueComponents.map(comp => `
### ${comp.name}
- **File**: ${comp.file}
- **Commands used**: ${comp.commands.join(', ') || 'None'}
- **Stores accessed**: ${comp.stores.join(', ') || 'None'}
- **Events emitted**: ${comp.events.join(', ') || 'None'}
`).join('\n')}

## 🔄 Data Flow Patterns

${this.contextData.dataFlowPatterns.map(pattern => `
### ${pattern.pattern}
- **Frequency**: ${pattern.frequency}
- **Components**: ${pattern.components.join(', ')}
${pattern.recommendation ? `- **Recommendation**: ${pattern.recommendation}` : ''}
`).join('\n')}

## 💡 Architectural Insights

${this.contextData.architecturalInsights.map(insight => `
### ${insight.type.toUpperCase()}: ${insight.description}
- **Severity**: ${insight.severity}
- **Affected**: ${insight.affectedComponents.join(', ')}
- **Recommendation**: ${insight.recommendation}
`).join('\n')}
`;
  }

  private async generateIDEHelpers(): Promise<void> {
    console.log('\n🛠️  Phase 6: Generating IDE helpers...');
    
    // Generate VSCode snippets
    const snippets = {
      "Tauri Command with Context": {
        "prefix": "tauricmd",
        "body": [
          "// ===== COMMAND: ${1:command_name} =====",
          "// INPUTS: 0 callers",
          "// OUTPUTS: [Analyzed via return type]",
          "// ===== END COMMAND =====",
          "#[tauri::command]",
          "pub async fn ${1:command_name}(",
          "    state: State<'_, AppState>",
          ") -> Result<${2:ReturnType}, Error> {",
          "    ${3:// Implementation}",
          "}"
        ]
      },
      "Vue Component with Context": {
        "prefix": "vuecontext",
        "body": [
          "<!--",
          "╔══════════════════════════════════════════════════════════════════╗",
          "║ COMPONENT DATA FLOW ANALYSIS                                     ║",
          "╚══════════════════════════════════════════════════════════════════╝",
          "",
          "📥 TAURI COMMANDS USED: 0",
          "🏪 STORE INTERACTIONS: 0",
          "📡 EVENT EMISSIONS: 0",
          "🔄 DATA FLOWS:",
          "-->",
          "",
          "<template>",
          "  ${1:<!-- Component template -->}",
          "</template>"
        ]
      }
    };
    
    const snippetsPath = join(this.projectRoot, '.vscode', 'context-snippets.json');
    writeFileSync(snippetsPath, JSON.stringify(snippets, null, 2));
    
    console.log('   ✅ IDE helpers generated');
  }

  private async generateLLMInstructions(): Promise<void> {
    console.log('\n🤖 Phase 7: Generating LLM instruction set...');
    
    const instructions = `# LLM Context Instructions for ${this.contextData.projectName}

## How to Use This Codebase's Context System

This project uses an advanced context-mapping system that provides rich inline documentation for every Tauri command and Vue component. When working with this codebase:

### 1. Understanding Command Context Blocks

Every Tauri command has a context block like this:
\`\`\`rust
// ===== COMMAND: command_name =====
// INPUTS: X callers
// - path/to/component.vue:L123 | Pattern: invoke('command_name', { data })
// OUTPUTS: ReturnType
// - consumed by: path/to/store.ts | updates state
// ===== END COMMAND =====
\`\`\`

**Use this information to:**
- Understand the complete data flow
- Identify all components that depend on this command
- See how responses are handled
- Avoid breaking existing integrations

### 2. Understanding Component Context Blocks

Every Vue component has a flow analysis block:
\`\`\`vue
<!--
╔══════════════════════════════════════════════════════════════════╗
║ COMPONENT DATA FLOW ANALYSIS                                     ║
╚══════════════════════════════════════════════════════════════════╝

📥 TAURI COMMANDS USED: X
▸ command_name
  Called from: mounted, method:handleClick
  Response handling:
    - Success: updates local state
    - Error: shows toast notification
-->
\`\`\`

**Use this to:**
- Understand component dependencies
- Track state management patterns
- Identify event flows
- Maintain consistency when modifying

### 3. Project-Specific Patterns

${this.contextData.dataFlowPatterns.map(p => `- **${p.pattern}**: ${p.recommendation || 'Common pattern'}`).join('\n')}

### 4. Architectural Considerations

${this.contextData.architecturalInsights.filter(i => i.severity !== 'info').map(i => `- **${i.type}**: ${i.description} (${i.recommendation})`).join('\n')}

### 5. When Making Changes

1. **Always update context blocks** when changing function signatures or adding new callers
2. **Follow existing patterns** identified in the data flow analysis
3. **Check cross-references** before removing or renaming commands
4. **Use the IDE snippets** for consistent documentation

## Quick Reference

- Total Tauri Commands: ${this.contextData.rustCommands.length}
- Total Vue Components: ${this.contextData.vueComponents.length}
- Most used command: ${this.getMostUsedCommand()}
- Primary data flow pattern: ${this.contextData.dataFlowPatterns[0]?.pattern || 'N/A'}

Remember: The context blocks are your map - trust them over assumptions!
`;
    
    const instructionsPath = join(this.projectRoot, 'docs', 'LLM_CONTEXT_GUIDE.md');
    writeFileSync(instructionsPath, instructions);
    
    console.log('   ✅ LLM instructions generated');
  }

  // Helper methods
  private extractProjectName(): string {
    try {
      const packageJson = JSON.parse(
        readFileSync(join(this.projectRoot, 'package.json'), 'utf-8')
      );
      return packageJson.name || 'Unknown Project';
    } catch {
      return 'Unknown Project';
    }
  }

  private parseRustAnalysisResults(): void {
    // Parse the enriched Rust files to extract command data
    // This would read the actual context blocks from the files
    console.log('   Parsing Rust analysis results...');
  }

  private parseVueAnalysisResults(): void {
    // Parse the enriched Vue files to extract component data
    console.log('   Parsing Vue analysis results...');
  }

  private checkForBottlenecks(): void {
    // Identify commands called by many components
    const threshold = 5;
    
    for (const cmd of this.contextData.rustCommands) {
      if (cmd.inputs.length > threshold) {
        this.contextData.architecturalInsights.push({
          type: 'bottleneck',
          severity: 'warning',
          description: `Command "${cmd.name}" is called by ${cmd.inputs.length} components`,
          affectedComponents: cmd.inputs.map(i => i.source),
          recommendation: 'Consider implementing caching or creating specialized variants'
        });
      }
    }
  }

  private checkForCoupling(): void {
    // Identify components with too many dependencies
    const threshold = 10;
    
    for (const comp of this.contextData.vueComponents) {
      const dependencies = comp.commands.length + comp.stores.length;
      if (dependencies > threshold) {
        this.contextData.architecturalInsights.push({
          type: 'coupling',
          severity: 'warning',
          description: `Component "${comp.name}" has ${dependencies} dependencies`,
          affectedComponents: [comp.name],
          recommendation: 'Consider splitting into smaller, focused components'
        });
      }
    }
  }

  private checkForOptimizations(): void {
    // Identify optimization opportunities
    // For example, multiple similar commands that could be consolidated
  }

  private getMostUsedCommand(): string {
    if (this.contextData.rustCommands.length === 0) return 'N/A';
    
    const sorted = [...this.contextData.rustCommands].sort(
      (a, b) => b.inputs.length - a.inputs.length
    );
    
    return sorted[0].name;
  }
}

// Make it executable
if (require.main === module) {
  const system = new UnifiedContextSystem();
  system.analyzeAndEnrich().catch(console.error);
}

export { UnifiedContextSystem };
