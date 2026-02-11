#!/usr/bin/env node
/**
 * xeto-doc-convert.js
 * Converts inline doc: tags to // comments above spec definitions
 *
 * Usage:
 *   node xeto-doc-convert.js <file-or-dir> [--preview]
 *
 * Examples:
 *   node xeto-doc-convert.js points.fans.xeto --preview   # preview single file
 *   node xeto-doc-convert.js points.fans.xeto             # convert single file
 *   node xeto-doc-convert.js .                            # convert all .xeto in cwd
 *   node xeto-doc-convert.js /path/to/dir --preview       # preview all .xeto in dir
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const PREVIEW = args.includes('--preview');
const target = args.find(a => !a.startsWith('--'));

if (!target) {
  console.log('Usage: node xeto-doc-convert.js <file-or-dir> [--preview]');
  process.exit(1);
}

/**
 * Process xeto content - finds specs with doc: inside braces, moves to comment above
 * Handles multi-line doc strings
 */
function convertContent(content) {
  const lines = content.split('\n');
  const result = [];
  let i = 0;
  let changeCount = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Match spec definition with opening brace: "SpecName: Parent & Other <abstract> {"
    const specMatch = line.match(/^(\s*)([A-Z][A-Za-z0-9_]*:\s*.+)\{\s*$/);

    if (specMatch) {
      const indent = specMatch[1];
      const specDef = specMatch[2].trimEnd();

      // Collect block content until closing brace
      const blockLines = [];
      let braceDepth = 1;
      let j = i + 1;

      while (j < lines.length && braceDepth > 0) {
        const blockLine = lines[j];
        // Track nested braces
        braceDepth += (blockLine.match(/\{/g) || []).length;
        braceDepth -= (blockLine.match(/\}/g) || []).length;

        if (braceDepth > 0) {
          blockLines.push(blockLine);
        }
        j++;
      }

      // Find and extract doc: line(s) - handles "doc: "multi\nline""
      let docValue = null;
      let docStartIdx = -1;
      let docEndIdx = -1;

      for (let k = 0; k < blockLines.length; k++) {
        const bl = blockLines[k];
        // Match doc: "..." (single line)
        const singleDocMatch = bl.match(/^\s*doc:\s*"([^"]*)"?\s*$/);
        if (singleDocMatch) {
          docValue = singleDocMatch[1];
          docStartIdx = k;
          docEndIdx = k;
          break;
        }
        // Match doc: "... (multi-line start)
        const multiDocStart = bl.match(/^\s*doc:\s*"([^"]*)\s*$/);
        if (multiDocStart) {
          docValue = multiDocStart[1];
          docStartIdx = k;
          // Find closing quote
          for (let m = k + 1; m < blockLines.length; m++) {
            const endMatch = blockLines[m].match(/^([^"]*)"\s*$/);
            if (endMatch) {
              docValue += '\n' + endMatch[1];
              docEndIdx = m;
              break;
            } else {
              docValue += '\n' + blockLines[m];
            }
          }
          break;
        }
      }

      if (docValue !== null) {
        changeCount++;

        // Remove doc line(s) from block
        const newBlockLines = [
          ...blockLines.slice(0, docStartIdx),
          ...blockLines.slice(docEndIdx + 1)
        ];

        // Build comment (handle multi-line)
        const docLines = docValue.split('\n');
        const comments = docLines.map(dl => `${indent}// ${dl}`).join('\n');

        // Check if block is now empty (only whitespace)
        const blockContent = newBlockLines.join('\n').trim();

        // Output: comment, then spec with block
        result.push(comments);
        result.push(`${indent}${specDef}{`);
        if (blockContent) {
          result.push(...newBlockLines);
        } else {
          result.push(`${indent}    `); // empty block with indent
        }
        result.push(lines[j - 1]); // closing brace line

        i = j;
        continue;
      }
    }

    result.push(line);
    i++;
  }

  return { content: result.join('\n'), changeCount };
}

/**
 * Process a single file
 */
function processFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const { content: newContent, changeCount } = convertContent(content);

  if (changeCount === 0) {
    return { changed: false, changeCount: 0 };
  }

  if (PREVIEW) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`FILE: ${filePath}`);
    console.log(`${'='.repeat(60)}`);
    console.log(newContent);
  } else {
    fs.writeFileSync(filePath, newContent, 'utf8');
  }

  return { changed: true, changeCount };
}

/**
 * Main
 */
function main() {
  const targetPath = path.resolve(target);
  const stat = fs.statSync(targetPath);

  let files = [];
  if (stat.isDirectory()) {
    files = fs.readdirSync(targetPath)
      .filter(f => f.endsWith('.xeto'))
      .map(f => path.join(targetPath, f));
  } else {
    files = [targetPath];
  }

  console.log(`${PREVIEW ? '[PREVIEW] ' : ''}Processing ${files.length} file(s)...\n`);

  let totalChanges = 0;
  for (const file of files) {
    const { changed, changeCount } = processFile(file);
    if (changed) {
      console.log(`${path.basename(file)}: ${changeCount} doc tag(s) ${PREVIEW ? 'found' : 'converted'}`);
      totalChanges += changeCount;
    }
  }

  console.log(`\nTotal: ${totalChanges} doc tag(s) ${PREVIEW ? 'would be converted' : 'converted'}`);
}

main();

