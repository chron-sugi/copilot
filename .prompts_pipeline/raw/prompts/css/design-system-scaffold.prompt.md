---
description: "Scaffold design system package structure and build configuration"
mode: 'agent'
tools: ['codebase', 'editor', 'terminal']
---

# Design System Scaffold Generator

Scaffold a complete design system package structure for: **${input:systemName:design-system}**

---

## Target Frameworks

Generate packages for: ${input:frameworks:CSS, React, Vue}

---

## Directory Structure to Create

```
${input:systemName}/
├── packages/
│   ├── tokens/                      # Design tokens package
│   │   ├── src/
│   │   │   ├── palette.json        # Tier 1: Raw palette tokens
│   │   │   ├── semantic.json       # Tier 2: Semantic tokens
│   │   │   ├── build.js            # Style Dictionary build script
│   │   │   └── config.json         # Style Dictionary config
│   │   ├── dist/                   # Build output (generated)
│   │   │   ├── css/
│   │   │   │   ├── palette.css
│   │   │   │   ├── semantic.css
│   │   │   │   └── themes/
│   │   │   │       ├── light.css
│   │   │   │       ├── dark.css
│   │   │   │       └── high-contrast.css
│   │   │   ├── scss/
│   │   │   │   ├── _palette.scss
│   │   │   │   └── _semantic.scss
│   │   │   ├── js/
│   │   │   │   └── tokens.js
│   │   │   └── json/
│   │   │       └── tokens.json
│   │   ├── package.json
│   │   └── README.md
│   │
│   ├── components/                  # Vanilla CSS components
│   │   ├── src/
│   │   │   ├── button/
│   │   │   │   ├── button.css
│   │   │   │   └── button.stories.js
│   │   │   ├── input/
│   │   │   │   ├── input.css
│   │   │   │   └── input.stories.js
│   │   │   └── index.css           # Barrel file
│   │   ├── dist/                   # Build output
│   │   ├── package.json
│   │   └── README.md
│   │
│   ├── react/                       # React component wrappers (if selected)
│   │   ├── src/
│   │   │   ├── Button/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Button.css      # Import from components pkg
│   │   │   │   └── Button.stories.jsx
│   │   │   └── index.js
│   │   ├── package.json
│   │   └── README.md
│   │
│   └── vue/                         # Vue component wrappers (if selected)
│       ├── src/
│       │   ├── Button/
│       │   │   └── Button.vue
│       │   └── index.js
│       ├── package.json
│       └── README.md
│
├── apps/
│   ├── docs/                        # Documentation site (Storybook or custom)
│   │   ├── .storybook/
│   │   │   ├── main.js
│   │   │   ├── preview.js
│   │   │   └── manager.js
│   │   ├── stories/
│   │   └── package.json
│   │
│   └── demo/                        # Demo app (optional)
│       └── package.json
│
├── .github/
│   └── workflows/
│       ├── ci.yml                   # CI pipeline
│       └── publish.yml              # NPM publish workflow
│
├── package.json                     # Monorepo root
├── pnpm-workspace.yaml              # Or npm workspaces config
├── turbo.json                       # Turborepo config (optional)
├── .gitignore
├── .eslintrc.js
├── .prettierrc.js
└── README.md
```

---

## File Generation Tasks

### 1. Root Configuration Files

**package.json** (monorepo root):
```json
{
  "name": "@${input:systemName}/monorepo",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "tokens:build": "pnpm --filter @${input:systemName}/tokens build",
    "storybook": "pnpm --filter docs storybook"
  },
  "devDependencies": {
    "turbo": "^latest",
    "prettier": "^latest",
    "eslint": "^latest"
  }
}
```

**pnpm-workspace.yaml** (or equivalent):
```yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

---

### 2. Tokens Package Files

**packages/tokens/package.json**:
```json
{
  "name": "@${input:systemName}/tokens",
  "version": "1.0.0",
  "description": "Design tokens for ${input:systemName}",
  "main": "dist/js/tokens.js",
  "types": "dist/js/tokens.d.ts",
  "files": ["dist"],
  "scripts": {
    "build": "node src/build.js",
    "watch": "node src/build.js --watch"
  },
  "devDependencies": {
    "style-dictionary": "^latest"
  }
}
```

**packages/tokens/src/config.json** (Style Dictionary):
```json
{
  "source": ["src/palette.json", "src/semantic.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "dist/css/",
      "files": [
        {
          "destination": "palette.css",
          "format": "css/variables",
          "filter": { "attributes": { "tier": "palette" } }
        },
        {
          "destination": "semantic.css",
          "format": "css/variables",
          "filter": { "attributes": { "tier": "semantic" } }
        }
      ]
    },
    "scss": {
      "transformGroup": "scss",
      "buildPath": "dist/scss/",
      "files": [
        {
          "destination": "_palette.scss",
          "format": "scss/variables"
        }
      ]
    },
    "js": {
      "transformGroup": "js",
      "buildPath": "dist/js/",
      "files": [
        {
          "destination": "tokens.js",
          "format": "javascript/es6"
        }
      ]
    }
  }
}
```

**packages/tokens/src/build.js**:
```javascript
const StyleDictionary = require('style-dictionary');
const config = require('./config.json');

console.log('Building design tokens...');

const sd = StyleDictionary.extend(config);
sd.buildAllPlatforms();

console.log('✅ Tokens built successfully');
```

**packages/tokens/src/palette.json** (starter):
```json
{
  "palette": {
    "blue": {
      "600": { "value": "#2563eb", "type": "color", "tier": "palette" }
    },
    "gray": {
      "50": { "value": "#f9fafb", "type": "color", "tier": "palette" },
      "900": { "value": "#111827", "type": "color", "tier": "palette" }
    },
    "spacing": {
      "4": { "value": "1rem", "type": "dimension", "tier": "palette" }
    }
  }
}
```

**packages/tokens/src/semantic.json** (starter):
```json
{
  "color": {
    "primary": { "value": "{palette.blue.600}", "type": "color", "tier": "semantic" },
    "surface": { "value": "{palette.gray.50}", "type": "color", "tier": "semantic" },
    "text": { "value": "{palette.gray.900}", "type": "color", "tier": "semantic" }
  },
  "spacing": {
    "md": { "value": "{palette.spacing.4}", "type": "dimension", "tier": "semantic" }
  }
}
```

---

### 3. Components Package Files

**packages/components/package.json**:
```json
{
  "name": "@${input:systemName}/components",
  "version": "1.0.0",
  "description": "Vanilla CSS components for ${input:systemName}",
  "main": "dist/index.css",
  "files": ["dist", "src"],
  "scripts": {
    "build": "postcss src/index.css -o dist/index.css",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  },
  "peerDependencies": {
    "@${input:systemName}/tokens": "^1.0.0"
  },
  "devDependencies": {
    "postcss": "^latest",
    "postcss-cli": "^latest",
    "@storybook/html": "^latest"
  }
}
```

**packages/components/src/button/button.css** (starter):
```css
@import '@${input:systemName}/tokens/dist/css/semantic.css';

@layer components {
  .c-button {
    --btn-bg: var(--color-primary);
    --btn-fg: var(--color-on-primary);
    --btn-padding-inline: var(--spacing-md);
    --btn-padding-block: var(--spacing-sm);

    background: var(--btn-bg);
    color: var(--btn-fg);
    padding-inline: var(--btn-padding-inline);
    padding-block: var(--btn-padding-block);
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
  }
}
```

---

### 4. Framework Packages (if selected)

**React package** (if ${input:frameworks} includes React):

**packages/react/package.json**:
```json
{
  "name": "@${input:systemName}/react",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "peerDependencies": {
    "react": "^18.0.0",
    "@${input:systemName}/components": "^1.0.0"
  }
}
```

**Vue package** (if ${input:frameworks} includes Vue):

**packages/vue/package.json**:
```json
{
  "name": "@${input:systemName}/vue",
  "version": "1.0.0",
  "main": "dist/index.js",
  "peerDependencies": {
    "vue": "^3.0.0",
    "@${input:systemName}/components": "^1.0.0"
  }
}
```

---

### 5. Documentation/Storybook Setup

**apps/docs/.storybook/preview.js**:
```javascript
import '@${input:systemName}/tokens/dist/css/semantic.css';
import '@${input:systemName}/tokens/dist/css/themes/light.css';
import '@${input:systemName}/components/dist/index.css';

export const parameters = {
  actions: { argTypesRegex: '^on[A-Z].*' },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
};
```

---

## Tasks to Execute

1. ✅ Create directory structure
2. ✅ Generate all package.json files
3. ✅ Create Style Dictionary configuration
4. ✅ Generate starter token files (palette.json, semantic.json)
5. ✅ Create starter component (button.css)
6. ✅ Set up Storybook configuration
7. ✅ Create README files for each package
8. ✅ Initialize git repository
9. ✅ Install dependencies: `pnpm install`
10. ✅ Build tokens: `pnpm tokens:build`

---

## Post-Scaffold Instructions

After scaffolding completes:

1. **Review generated files** in each package
2. **Customize tokens** in `packages/tokens/src/`
3. **Add components** to `packages/components/src/`
4. **Run Storybook**: `pnpm storybook`
5. **Build all packages**: `pnpm build`

---

**Related:**
- [Design System Architecture](../../docs/design-system-architecture.md)
- [Style Dictionary Documentation](https://amzn.github.io/style-dictionary/)
