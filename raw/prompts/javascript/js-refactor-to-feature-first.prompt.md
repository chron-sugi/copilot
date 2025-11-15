---
description: "Migrate from component-first to feature-first architecture with step-by-step instructions"
mode: 'agent'
tools: ['codebase', 'edit', 'terminal', 'search']
---

# Refactor to Feature-First Architecture

Migrate your codebase from component-first (or other structure) to feature-first architecture.

---

## Current Structure Assessment

**Current folder structure**: ${input:currentStructure:components/, hooks/, api/, utils/}

**Target feature**: ${input:featureName:cart}

**Files to migrate**: ${input:filesToMigrate:List files that belong to this feature}

---

## Migration Strategy

### Step 1: Analyze Current Structure

Identify all files related to the feature:

**Component-First Structure:**
```
src/
  components/
    CartPanel.tsx
    CartItem.tsx
  hooks/
    useCart.ts
  api/
    cart-api.ts
  utils/
    cart-utils.ts
```

**Feature-First Structure (Target):**
```
src/
  features/
    cart/
      components/
        CartPanel/
          CartPanel.tsx
          CartPanel.test.tsx
        CartItem/
          CartItem.tsx
          CartItem.test.tsx
      hooks/
        useCart.ts
        useCart.test.ts
      api/
        get-cart.ts
        update-cart.ts
      model/
        cart.types.ts
        cart.schema.ts
      services/
        cart.service.ts
        cart.service.test.ts
      index.ts
```

---

## Migration Steps

### Step 1: Create Feature Folder Structure

```bash
# Create feature folders
mkdir -p src/features/${featureName}/{components,hooks,api,model,services}
```

### Step 2: Move Component Files

```bash
# Move components into feature folder
# Create component folders for better organization
mkdir -p src/features/${featureName}/components/${ComponentName}
mv src/components/${ComponentName}.tsx src/features/${featureName}/components/${ComponentName}/
mv src/components/${ComponentName}.test.tsx src/features/${featureName}/components/${ComponentName}/ 2>/dev/null || true
mv src/components/${ComponentName}.module.css src/features/${featureName}/components/${ComponentName}/ 2>/dev/null || true
```

### Step 3: Move Hooks

```bash
# Move hooks
mv src/hooks/use${FeatureName}.ts src/features/${featureName}/hooks/
mv src/hooks/use${FeatureName}.test.ts src/features/${featureName}/hooks/ 2>/dev/null || true
```

### Step 4: Split and Move API Files

If you have a large API file, split it:

```typescript
// Before: src/api/cart-api.ts (300 lines)
export function getCart() { }
export function updateCart() { }
export function addItem() { }
export function removeItem() { }

// After: Split by operation
// src/features/cart/api/get-cart.ts (50 lines)
export function getCart() { }

// src/features/cart/api/update-cart.ts (40 lines)
export function updateCart() { }
export function addItem() { }
export function removeItem() { }
```

### Step 5: Extract Types and Schemas

```bash
# Create model folder for types and schemas
mkdir -p src/features/${featureName}/model

# Move or create type files
mv src/types/${featureName}.types.ts src/features/${featureName}/model/ 2>/dev/null || true
```

**Create runtime schema** (if not exists):

```typescript
// src/features/${featureName}/model/${featureName}.schema.ts
import { z } from 'zod';

export const ${FeatureName}Item = z.object({
  id: z.string(),
  name: z.string(),
  // ... other fields
});

export const ${FeatureName} = z.object({
  items: z.array(${FeatureName}Item),
});

export type ${FeatureName} = z.infer<typeof ${FeatureName}>;
export type ${FeatureName}Item = z.infer<typeof ${FeatureName}Item>;
```

### Step 6: Create Service Layer

```typescript
// src/features/${featureName}/services/${featureName}.service.ts
import { get${FeatureName} } from '../api/get-${featureName}';

export async function load${FeatureName}Summary(id: string) {
  const ${featureName} = await get${FeatureName}(id);
  // Add orchestration logic here
  return {
    count: ${featureName}.items.length,
    // ... computed values
  };
}
```

### Step 7: Update Imports Incrementally

**Before:**
```typescript
import { CartPanel } from '@/components/CartPanel';
import { useCart } from '@/hooks/useCart';
import { getCart } from '@/api/cart-api';
```

**After:**
```typescript
import { CartPanel, useCart, getCart } from '@/features/cart';
```

**Update process:**
1. Search for all imports from old locations
2. Update to new feature-based imports
3. Verify no broken imports

```bash
# Find all imports to update
grep -r "from '@/components/Cart" src/
grep -r "from '@/hooks/useCart" src/
grep -r "from '@/api/cart-api" src/
```

### Step 8: Create Public API (Barrel File)

```typescript
// src/features/${featureName}/index.ts
// Export public API only

// Components
export { CartPanel } from './components/CartPanel/CartPanel';
export { CartItem } from './components/CartItem/CartItem';

// Hooks
export { useCart } from './hooks/useCart';

// API
export { getCart } from './api/get-cart';
export { updateCart, addItem, removeItem } from './api/update-cart';

// Types & Schemas
export type { Cart, CartItem } from './model/cart.types';
export { CartSchema, CartItemSchema } from './model/cart.schema';

// Services
export { loadCartSummary } from './services/cart.service';
```

### Step 9: Run Tests

```bash
# Verify all tests still pass
npm run test

# Check for circular dependencies
npx madge --circular --extensions ts,tsx src/

# Type check
npm run typecheck
```

### Step 10: Remove Old Files

**Only after all imports are updated and tests pass:**

```bash
# Remove old component files
rm src/components/Cart*.tsx

# Remove old hook files
rm src/hooks/useCart.ts

# Remove old API files
rm src/api/cart-api.ts

# Remove old utility files (if moved to services)
rm src/utils/cart-utils.ts
```

---

## Migration Checklist

### Pre-Migration
- [ ] Identify all files belonging to the feature
- [ ] Run tests to establish baseline
- [ ] Create feature branch: `git checkout -b refactor/${featureName}-feature-first`

### During Migration
- [ ] Create feature folder structure
- [ ] Move component files with tests and styles
- [ ] Move hook files with tests
- [ ] Split large API files by operation
- [ ] Extract types and create schemas
- [ ] Create service layer for orchestration
- [ ] Create public API barrel file (index.ts)
- [ ] Update all imports incrementally
- [ ] Run tests after each major change

### Post-Migration
- [ ] All tests passing
- [ ] No circular dependencies (`madge`)
- [ ] TypeScript compiles without errors
- [ ] No broken imports
- [ ] Old files removed
- [ ] Documentation updated

---

## Common Pitfalls

### 1. Import Paths Break

**Problem**: Relative imports become incorrect after moving files

**Solution**: Update incrementally, run tests frequently

```typescript
// Before (in src/components/CartPanel.tsx)
import { useCart } from '../hooks/useCart';

// After (in src/features/cart/components/CartPanel/CartPanel.tsx)
import { useCart } from '../../hooks/useCart';
// OR better: use public API
import { useCart } from '@/features/cart';
```

### 2. Circular Dependencies Introduced

**Problem**: Feature imports from itself through barrel file

**Solution**: Import directly from source file within feature

```typescript
// ❌ Inside feature, don't use barrel
import { useCart } from '../index';  // Circular!

// ✅ Import directly
import { useCart } from '../hooks/useCart';
```

### 3. Forgotten Test Files

**Problem**: Tests left in old location

**Solution**: Always move tests with source files

```bash
# Move components with all related files
mv src/components/CartPanel.tsx src/features/cart/components/CartPanel/
mv src/components/CartPanel.test.tsx src/features/cart/components/CartPanel/
mv src/components/CartPanel.module.css src/features/cart/components/CartPanel/
```

### 4. Large Barrel Files Hurt Tree-Shaking

**Problem**: `export *` imports everything

**Solution**: Use explicit named exports

```typescript
// ❌ Imports entire module graph
export * from './components';
export * from './hooks';

// ✅ Explicit exports only
export { CartPanel } from './components/CartPanel/CartPanel';
export { useCart } from './hooks/useCart';
```

---

## Incremental Migration Strategy

### Option 1: Migrate One Feature at a Time (Recommended)

**Advantages:**
- Low risk (small changes)
- Easy to review
- Can roll back easily
- Continuous delivery

**Process:**
1. Migrate cart feature
2. Update imports for cart
3. Test and commit
4. Migrate user feature
5. Update imports for user
6. Test and commit
7. Continue until all features migrated

### Option 2: Parallel Structure (Temporary)

**Advantages:**
- Old code continues to work
- Can migrate at own pace
- No breaking changes during migration

**Process:**
1. Create new `features/` alongside old `components/`
2. Create new files in `features/` (don't move yet)
3. Deprecate old imports with JSDoc
4. Gradually update imports
5. Remove old structure when fully migrated

```typescript
/**
 * @deprecated Use @/features/cart instead
 */
export { CartPanel } from '@/components/CartPanel';
```

---

## Validation

After migration, verify:

```bash
# 1. No circular dependencies
npx madge --circular --extensions ts,tsx src/
# Should output: "✓ No circular dependencies found"

# 2. All tests pass
npm run test
# Should show all green

# 3. TypeScript compiles
npm run typecheck
# Should have no errors

# 4. Build succeeds
npm run build
# Should complete successfully

# 5. Bundle size acceptable
npm run analyze
# Check bundle size didn't increase significantly
```

---

## Rollback Plan

If migration causes issues:

```bash
# 1. Revert changes
git reset --hard HEAD

# 2. Or cherry-pick working commits
git revert <commit-hash>

# 3. Or restore from backup branch
git checkout main
git branch -D refactor/${featureName}-feature-first
```

---

**Related**:
- [JavaScript Core Standards](../../instructions/javascript.instructions.md)
- [JavaScript Web Application Playbook](../../docs/javascript-web-app-playbook.md)
- [JS Refactorer Mode](../../chatmodes/javascript/js-refactorer.chatmode.md)
- [JS Create Feature](./js-create-feature.prompt.md)
