---
description: "Generate feature-first folder structure with templates for components, API, services, and tests"
mode: 'agent'
tools: ['codebase', 'edit', 'terminal']
---

# Create JavaScript Feature

Generate a new feature with complete folder structure, templates, and tests.

---

## Feature Details

**Feature name**: ${input:featureName:cart}

**Description**: ${input:description:Brief description of what this feature does}

**API endpoints**: ${input:apiEndpoints:get-feature, update-feature}

**Data models**: ${input:dataModels:FeatureItem, Feature}

---

## Generate Feature Structure

Create the following feature-first structure:

```
features/${featureName}/
  ├── components/
  │   └── ${FeatureName}Panel/
  │       ├── ${FeatureName}Panel.tsx
  │       ├── ${FeatureName}Panel.test.tsx
  │       └── ${FeatureName}Panel.module.css
  ├── hooks/
  │   ├── use${FeatureName}.ts
  │   └── use${FeatureName}.test.ts
  ├── api/
  │   ├── get-${featureName}.ts
  │   └── update-${featureName}.ts
  ├── model/
  │   ├── ${featureName}.types.ts
  │   ├── ${featureName}.schema.ts
  │   └── ${featureName}.selectors.ts
  ├── services/
  │   ├── ${featureName}.service.ts
  │   └── ${featureName}.service.test.ts
  └── index.ts
```

---

## File Templates

### 1. Data Schema (model/${featureName}.schema.ts)

```typescript
import { z } from 'zod';

export const ${FeatureName}Item = z.object({
  id: z.string(),
  name: z.string(),
  status: z.enum(['active', 'inactive']),
  createdAt: z.string().datetime(),
});

export const ${FeatureName} = z.object({
  id: z.string(),
  items: z.array(${FeatureName}Item),
  total: z.number().nonnegative(),
});

export type ${FeatureName} = z.infer<typeof ${FeatureName}>;
export type ${FeatureName}Item = z.infer<typeof ${FeatureName}Item>;
```

### 2. TypeScript Types (model/${featureName}.types.ts)

```typescript
export type { ${FeatureName}, ${FeatureName}Item } from './${featureName}.schema';

// Additional types not in schema
export interface ${FeatureName}ListParams {
  page?: number;
  limit?: number;
  sortBy?: string;
}

export interface ${FeatureName}Summary {
  count: number;
  activeCount: number;
}
```

### 3. API Layer with DI (api/get-${featureName}.ts)

```typescript
import { ${FeatureName} } from '../model/${featureName}.schema';
import { HttpError } from '@/shared/lib/errors';

type Deps = {
  fetchFn?: typeof fetch;
  signal?: AbortSignal;
};

export async function get${FeatureName}(
  id: string,
  { fetchFn = fetch, signal }: Deps = {}
): Promise<${FeatureName}> {
  const res = await fetchFn(`/api/${featureName}s/\${id}`, {
    headers: { 'Accept': 'application/json' },
    signal,
  });

  if (!res.ok) {
    throw new HttpError(
      `Failed to load ${featureName}: \${res.status}`,
      res.status
    );
  }

  const json = await res.json();
  return ${FeatureName}.parse(json); // Runtime validation
}
```

### 4. Service Layer (services/${featureName}.service.ts)

```typescript
import { get${FeatureName} } from '../api/get-${featureName}';
import type { ${FeatureName}Summary } from '../model/${featureName}.types';

type Deps = Parameters<typeof get${FeatureName}>[1];

export async function load${FeatureName}Summary(
  id: string,
  deps?: Deps
): Promise<${FeatureName}Summary> {
  const ${featureName} = await get${FeatureName}(id, deps);

  return {
    count: ${featureName}.items.length,
    activeCount: ${featureName}.items.filter(item => item.status === 'active').length,
  };
}
```

### 5. React Hook (hooks/use${FeatureName}.ts)

```typescript
import { useQuery } from '@tanstack/react-query';
import { get${FeatureName} } from '../api/get-${featureName}';

export function use${FeatureName}(id: string) {
  return useQuery({
    queryKey: ['${featureName}', id],
    queryFn: () => get${FeatureName}(id),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

### 6. React Component (components/${FeatureName}Panel/${FeatureName}Panel.tsx)

```typescript
import { use${FeatureName} } from '../../hooks/use${FeatureName}';
import styles from './${FeatureName}Panel.module.css';

interface ${FeatureName}PanelProps {
  id: string;
}

export function ${FeatureName}Panel({ id }: ${FeatureName}PanelProps) {
  const { data: ${featureName}, isLoading, error } = use${FeatureName}(id);

  if (isLoading) return <div className={styles.loading}>Loading...</div>;
  if (error) return <div className={styles.error}>Error loading ${featureName}</div>;
  if (!${featureName}) return null;

  return (
    <div className={styles.panel}>
      <h2 className={styles.title}>{${featureName}.items.length} Items</h2>
      <ul className={styles.list}>
        {${featureName}.items.map(item => (
          <li key={item.id} className={styles.item}>
            {item.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### 7. Service Tests (services/${featureName}.service.test.ts)

```typescript
import { load${FeatureName}Summary } from './${featureName}.service';
import { build${FeatureName} } from '@/shared/test-utils/builders';

describe('load${FeatureName}Summary', () => {
  test('computes count and activeCount', async () => {
    const mock${FeatureName} = build${FeatureName}({
      items: [
        { id: '1', name: 'A', status: 'active', createdAt: '2025-01-01T00:00:00Z' },
        { id: '2', name: 'B', status: 'inactive', createdAt: '2025-01-02T00:00:00Z' },
      ],
    });

    const fetchFn = async () =>
      new Response(JSON.stringify(mock${FeatureName}), { status: 200 });

    const result = await load${FeatureName}Summary('123', { fetchFn });

    expect(result).toEqual({ count: 2, activeCount: 1 });
  });

  test('throws on network error', async () => {
    const fetchFn = async () => new Response(null, { status: 500 });

    await expect(load${FeatureName}Summary('123', { fetchFn }))
      .rejects.toThrow('Failed to load ${featureName}: 500');
  });
});
```

### 8. Component Tests (components/${FeatureName}Panel/${FeatureName}Panel.test.tsx)

```typescript
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ${FeatureName}Panel } from './${FeatureName}Panel';

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

function renderWithClient(ui: React.ReactElement) {
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  );
}

describe('${FeatureName}Panel', () => {
  test('renders loading state', () => {
    renderWithClient(<${FeatureName}Panel id="123" />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders ${featureName} items', async () => {
    // Mock API response
    global.fetch = vi.fn(() =>
      Promise.resolve(new Response(JSON.stringify({
        id: '123',
        items: [
          { id: '1', name: 'Item 1', status: 'active', createdAt: '2025-01-01T00:00:00Z' },
        ],
        total: 1,
      })))
    );

    renderWithClient(<${FeatureName}Panel id="123" />);

    expect(await screen.findByText('1 Items')).toBeInTheDocument();
    expect(screen.getByText('Item 1')).toBeInTheDocument();
  });
});
```

### 9. Public API (index.ts)

```typescript
// Components
export { ${FeatureName}Panel } from './components/${FeatureName}Panel/${FeatureName}Panel';

// Hooks
export { use${FeatureName} } from './hooks/use${FeatureName}';

// API
export { get${FeatureName} } from './api/get-${featureName}';

// Types & Schemas
export type { ${FeatureName}, ${FeatureName}Item, ${FeatureName}Summary } from './model/${featureName}.types';
export { ${FeatureName}Schema, ${FeatureName}ItemSchema } from './model/${featureName}.schema';

// Services
export { load${FeatureName}Summary } from './services/${featureName}.service';
```

---

## Test Data Factory

Also create test data factory in `shared/test-utils/builders.ts`:

```typescript
import { faker } from '@faker-js/faker';
import type { ${FeatureName}, ${FeatureName}Item } from '@/features/${featureName}';

export const build${FeatureName}Item = (
  overrides: Partial<${FeatureName}Item> = {}
): ${FeatureName}Item => ({
  id: faker.string.uuid(),
  name: faker.commerce.productName(),
  status: faker.helpers.arrayElement(['active', 'inactive']),
  createdAt: faker.date.past().toISOString(),
  ...overrides,
});

export const build${FeatureName} = (
  overrides: Partial<${FeatureName}> = {}
): ${FeatureName} => ({
  id: faker.string.uuid(),
  items: [],
  total: 0,
  ...overrides,
});
```

---

## Checklist

After generation, verify:

- [ ] All files created in correct folders
- [ ] Named exports used throughout
- [ ] Dependency injection applied to API layer
- [ ] Runtime validation with Zod schemas
- [ ] Tests include error paths
- [ ] Test data factories created
- [ ] Public API exported in index.ts
- [ ] No circular dependencies
- [ ] Modules ≤200 lines

---

**Related**:
- [JavaScript Core Standards](../../instructions/javascript.instructions.md)
- [JavaScript Web Application Playbook](../../docs/javascript-web-app-playbook.md)
- [JS Developer Mode](../../chatmodes/javascript/js-developer.chatmode.md)
