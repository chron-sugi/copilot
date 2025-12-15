# Follow these instructions

Do not stop after finding one issue.REVIEW THE ENTIRE CHECKLIST in the React frontend guide and verify EVERY item before proposing fixes. List each checklist item and its status (pass, fail, needs review) before making any code changes.

# React Frontend Implementation & Debugging Guide

Comprehensive reference for building React applications with TanStack Query, TanStack Table, and URL state management. Use this guide to verify implementations and debug issues.

---

## Table of Contents

1. [React Hooks Rules](#react-hooks-rules)
2. [TanStack Query](#tanstack-query)
3. [TanStack Table](#tanstack-table)
4. [URL State Management](#url-state-management)
5. [Component Patterns](#component-patterns)
6. [Common Errors & Fixes](#common-errors--fixes)
7. [Debugging Methodology](#debugging-methodology)
8. [Integration Patterns](#integration-patterns)
9. [Performance Considerations](#performance-considerations)
10. [Checklist](#checklist)

---

## React Hooks Rules

### Fundamental Rules (Never Violate)

1. **Only call hooks at the top level** - Never inside loops, conditions, or nested functions
2. **Only call hooks from React functions** - Components or custom hooks only
3. **Hooks must run in the same order every render** - No conditional hook calls

### Correct Hook Ordering

```tsx
function Component({ id, enabled }) {
  // ✅ ALL HOOKS FIRST - before any conditional logic
  const [state, setState] = useState(initialValue);
  const [otherState, setOtherState] = useState(null);
  const queryResult = useQuery({ queryKey: ['data', id], queryFn: fetchData });
  const ref = useRef(null);
  const memoizedValue = useMemo(() => compute(state), [state]);
  const memoizedCallback = useCallback(() => doThing(state), [state]);
  
  useEffect(() => {
    // side effect
  }, [dependency]);

  // ✅ CONDITIONAL RETURNS AFTER ALL HOOKS
  if (!enabled) return null;
  if (queryResult.isLoading) return <Spinner />;
  if (queryResult.isError) return <Error />;

  // ✅ RENDER
  return <div>{/* content */}</div>;
}
```

### Incorrect Patterns (Will Break)

```tsx
function Component({ id, enabled }) {
  // ❌ WRONG: Conditional hook - breaks rules of hooks
  if (enabled) {
    const [state, setState] = useState(null);
  }

  // ❌ WRONG: Early return before hooks
  if (!id) return <Error />;
  
  const queryResult = useQuery(...); // This hook won't run if id is falsy

  // ❌ WRONG: Hook inside condition
  if (someCondition) {
    useEffect(() => {}, []);
  }

  // ❌ WRONG: Hook inside loop
  items.forEach(item => {
    const [itemState] = useState(item);
  });
}
```

### useState

```tsx
// Basic usage
const [value, setValue] = useState(initialValue);

// Lazy initialization (for expensive computations)
const [value, setValue] = useState(() => computeExpensiveInitialValue());

// Updating based on previous value
setValue(prev => prev + 1);

// Object state - must spread to maintain other properties
const [form, setForm] = useState({ name: '', email: '' });
setForm(prev => ({ ...prev, name: 'New Name' }));

// Array state
const [items, setItems] = useState([]);
setItems(prev => [...prev, newItem]); // Add
setItems(prev => prev.filter(item => item.id !== idToRemove)); // Remove
setItems(prev => prev.map(item => item.id === id ? { ...item, updated: true } : item)); // Update
```

### useEffect

```tsx
// Runs on every render (rarely wanted)
useEffect(() => {
  console.log('Runs every render');
});

// Runs once on mount
useEffect(() => {
  console.log('Runs once on mount');
}, []);

// Runs when dependencies change
useEffect(() => {
  console.log('Runs when id changes');
}, [id]);

// Cleanup function
useEffect(() => {
  const subscription = subscribe(id);
  return () => {
    subscription.unsubscribe(); // Cleanup runs before next effect and on unmount
  };
}, [id]);

// ❌ WRONG: Missing dependency (stale closure)
useEffect(() => {
  doSomething(id); // Uses id but id not in deps
}, []); // ESLint will warn

// ❌ WRONG: Object/array dependency (new reference every render)
useEffect(() => {
  doSomething(options);
}, [options]); // If options is { a: 1 }, it's a new object each render = infinite loop

// ✅ FIX: Destructure or memoize
useEffect(() => {
  doSomething(optionA, optionB);
}, [optionA, optionB]); // Primitive values are stable
```

### useCallback

Memoizes a function so it maintains referential equality between renders.

```tsx
// Without useCallback - new function every render
const handleClick = () => {
  doSomething(id);
};

// With useCallback - same function reference if id hasn't changed
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// WHEN TO USE:
// 1. Passing callbacks to child components that use React.memo
// 2. Passing callbacks as dependencies to useEffect
// 3. Passing callbacks to components that compare props (like filter components)

// ❌ WRONG: Missing dependency
const handleClick = useCallback(() => {
  doSomething(id); // Uses id
}, []); // id missing - stale closure

// ✅ CORRECT: All dependencies included
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

### useMemo

Memoizes a computed value.

```tsx
// Without useMemo - recomputes every render
const sortedItems = items.sort((a, b) => a.name.localeCompare(b.name));

// With useMemo - only recomputes when items changes
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// WHEN TO USE:
// 1. Expensive computations
// 2. Creating objects/arrays passed as props or dependencies
// 3. Derived data from props or state

// Creating stable object reference
const options = useMemo(() => ({
  threshold: 0.5,
  enabled: isEnabled,
}), [isEnabled]);
```

### useRef

```tsx
// DOM reference
const inputRef = useRef<HTMLInputElement>(null);
// Usage: <input ref={inputRef} />
// Access: inputRef.current?.focus()

// Mutable value that doesn't trigger re-render
const previousValueRef = useRef(value);
useEffect(() => {
  previousValueRef.current = value;
}, [value]);

// Store interval/timeout IDs
const intervalRef = useRef<number | null>(null);
useEffect(() => {
  intervalRef.current = setInterval(() => {}, 1000);
  return () => {
    if (intervalRef.current) clearInterval(intervalRef.current);
  };
}, []);
```

---

## TanStack Query

### Setup

```tsx
// App.tsx or main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  );
}
```

### useQuery

```tsx
import { useQuery } from '@tanstack/react-query';

function Component({ id }) {
  const {
    data,        // The resolved data (undefined until success)
    isLoading,   // True on first load with no data
    isFetching,  // True whenever a request is in flight
    isError,     // True if query failed
    error,       // The error object if failed
    isSuccess,   // True if query succeeded
    refetch,     // Function to manually refetch
    status,      // 'pending' | 'error' | 'success'
  } = useQuery({
    queryKey: ['items', id],          // Unique key - refetches when this changes
    queryFn: () => fetchItems(id),    // Function that returns a promise
    enabled: !!id,                     // Only run query if id exists
    staleTime: 1000 * 60 * 5,         // Data considered fresh for 5 min
    gcTime: 1000 * 60 * 30,           // Cache garbage collected after 30 min
    retry: 3,                          // Retry failed requests 3 times
    refetchOnWindowFocus: false,       // Don't refetch when window regains focus
  });

  // Handle states
  if (isLoading) return <Spinner />;
  if (isError) return <Error message={error.message} />;
  if (!data) return <Empty />;
  
  return <List items={data.items} />;
}
```

### Query Keys

Query keys determine cache identity and when queries refetch.

```tsx
// Simple key
useQuery({ queryKey: ['todos'], queryFn: fetchTodos });

// Key with variable - refetches when id changes
useQuery({ queryKey: ['todo', id], queryFn: () => fetchTodo(id) });

// Key with object - refetches when any property changes
useQuery({
  queryKey: ['todos', { status, page, pageSize }],
  queryFn: () => fetchTodos({ status, page, pageSize }),
});

// ❌ WRONG: Variable used in queryFn but not in queryKey
useQuery({
  queryKey: ['todos'], // Missing filter
  queryFn: () => fetchTodos(filter), // Uses filter - won't refetch when filter changes
});

// ✅ CORRECT: All variables in both
useQuery({
  queryKey: ['todos', filter],
  queryFn: () => fetchTodos(filter),
});
```

### The `enabled` Option

Controls whether the query runs.

```tsx
// Only fetch when id exists
useQuery({
  queryKey: ['item', id],
  queryFn: () => fetchItem(id),
  enabled: !!id, // Converts to boolean - false if id is undefined/null/''
});

// Dependent queries - wait for first query
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => fetchProjects(user.id),
  enabled: !!user?.id, // Only runs after user is loaded
});

// Multiple conditions
useQuery({
  queryKey: ['data', id, filters],
  queryFn: () => fetchData(id, filters),
  enabled: !!id && isFeatureEnabled && !isPaused,
});
```

### useMutation

For creating, updating, or deleting data.

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function Component() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newItem) => createItem(newItem),
    onSuccess: (data, variables) => {
      // Invalidate and refetch related queries
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
    onError: (error, variables, context) => {
      console.error('Failed to create item:', error);
    },
  });

  const handleSubmit = (data) => {
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      {mutation.isPending && <Spinner />}
      {mutation.isError && <Error message={mutation.error.message} />}
      {mutation.isSuccess && <Success />}
      <button type="submit" disabled={mutation.isPending}>
        Submit
      </button>
    </form>
  );
}
```

### Common Query Patterns

```tsx
// Pagination
function PaginatedList() {
  const [page, setPage] = useState(1);
  
  const { data, isLoading, isPlaceholderData } = useQuery({
    queryKey: ['items', page],
    queryFn: () => fetchItems(page),
    placeholderData: keepPreviousData, // Keep showing old data while fetching new page
  });

  return (
    <div style={{ opacity: isPlaceholderData ? 0.5 : 1 }}>
      {data?.items.map(item => <Item key={item.id} item={item} />)}
      <button onClick={() => setPage(p => p - 1)} disabled={page === 1}>
        Previous
      </button>
      <button onClick={() => setPage(p => p + 1)} disabled={!data?.hasMore}>
        Next
      </button>
    </div>
  );
}

// Polling
useQuery({
  queryKey: ['status'],
  queryFn: fetchStatus,
  refetchInterval: 5000, // Refetch every 5 seconds
  refetchIntervalInBackground: true, // Continue polling when tab is hidden
});
```

---

## TanStack Table

### Core Concept

TanStack Table is headless - it provides logic, you provide UI.

```tsx
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  flexRender,
  type ColumnDef,
} from '@tanstack/react-table';
```

### Basic Setup

```tsx
// 1. Define columns OUTSIDE the component or memoize them
const columns: ColumnDef<Person>[] = [
  {
    accessorKey: 'name',      // Key in data object
    header: 'Name',           // Column header text
  },
  {
    accessorKey: 'email',
    header: 'Email',
  },
  {
    accessorKey: 'age',
    header: 'Age',
    cell: ({ getValue }) => `${getValue()} years`, // Custom cell render
  },
];

// 2. Use in component
function Table({ data }: { data: Person[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(), // Required
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map(headerGroup => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map(header => (
              <th key={header.id}>
                {flexRender(header.column.columnDef.header, header.getContext())}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map(row => (
          <tr key={row.id}>
            {row.getVisibleCells().map(cell => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Column Definitions

```tsx
const columns: ColumnDef<DataType>[] = [
  // Simple accessor
  {
    accessorKey: 'name',
    header: 'Name',
  },

  // Accessor function for nested data
  {
    accessorFn: row => row.user.name,
    id: 'userName', // Required when using accessorFn
    header: 'User Name',
  },

  // Custom header
  {
    accessorKey: 'status',
    header: () => <span className="font-bold">Status</span>,
  },

  // Custom cell
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ getValue }) => {
      const status = getValue<string>();
      return <Badge variant={status}>{status}</Badge>;
    },
  },

  // Cell with row data
  {
    accessorKey: 'actions',
    header: 'Actions',
    cell: ({ row }) => (
      <button onClick={() => handleEdit(row.original)}>
        Edit {row.original.name}
      </button>
    ),
  },

  // With meta for custom data
  {
    accessorKey: 'vendor',
    header: 'Vendor',
    meta: {
      filterType: 'select',
      filterOptions: vendors,
    },
  },
];
```

### CRITICAL: Column Definition Stability

Columns must be stable references. If columns are recreated every render, the table breaks.

```tsx
// ❌ WRONG: Columns defined inside component - new array every render
function Table({ data }) {
  const columns = [
    { accessorKey: 'name', header: 'Name' },
  ];
  
  const table = useReactTable({ data, columns, ... });
}

// ✅ CORRECT: Columns defined outside component
const columns = [
  { accessorKey: 'name', header: 'Name' },
];

function Table({ data }) {
  const table = useReactTable({ data, columns, ... });
}

// ✅ CORRECT: Columns memoized if they depend on props
function Table({ data, onEdit }) {
  const columns = useMemo(() => [
    { accessorKey: 'name', header: 'Name' },
    {
      id: 'actions',
      cell: ({ row }) => <button onClick={() => onEdit(row.original)}>Edit</button>,
    },
  ], [onEdit]);
  
  const table = useReactTable({ data, columns, ... });
}
```

### Sorting

```tsx
import { getSortedRowModel, type SortingState } from '@tanstack/react-table';

function Table({ data }) {
  const [sorting, setSorting] = useState<SortingState>([]);

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  // In header render
  <th
    onClick={header.column.getToggleSortingHandler()}
    style={{ cursor: header.column.getCanSort() ? 'pointer' : 'default' }}
  >
    {flexRender(header.column.columnDef.header, header.getContext())}
    {{ asc: ' 🔼', desc: ' 🔽' }[header.column.getIsSorted() as string] ?? null}
  </th>
}
```

### Filtering

```tsx
import { getFilteredRowModel, type ColumnFiltersState } from '@tanstack/react-table';

function Table({ data }) {
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);

  const table = useReactTable({
    data,
    columns,
    state: { columnFilters },
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  // Set a filter
  table.getColumn('status')?.setFilterValue('active');

  // Get current filter value
  const statusFilter = table.getColumn('status')?.getFilterValue();

  // Clear a filter
  table.getColumn('status')?.setFilterValue(undefined);
}
```

### Pagination

```tsx
import { getPaginationRowModel, type PaginationState } from '@tanstack/react-table';

function Table({ data }) {
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0, // 0-indexed
    pageSize: 10,
  });

  const table = useReactTable({
    data,
    columns,
    state: { pagination },
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <>
      <table>{/* ... */}</table>
      
      <div>
        <button
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </button>
        <span>
          Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
        </span>
        <button
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </button>
        <select
          value={table.getState().pagination.pageSize}
          onChange={e => table.setPageSize(Number(e.target.value))}
        >
          {[10, 25, 50, 100].map(size => (
            <option key={size} value={size}>{size} per page</option>
          ))}
        </select>
      </div>
    </>
  );
}
```

### Column Visibility

```tsx
import { type VisibilityState } from '@tanstack/react-table';

function Table({ data }) {
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({
    email: false, // Hidden by default
    phone: false,
  });

  const table = useReactTable({
    data,
    columns,
    state: { columnVisibility },
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
  });

  // Toggle visibility
  table.getColumn('email')?.toggleVisibility();

  // Get all columns for visibility UI
  const allColumns = table.getAllLeafColumns();

  return (
    <>
      {/* Column visibility dropdown */}
      <div>
        {allColumns.map(column => (
          <label key={column.id}>
            <input
              type="checkbox"
              checked={column.getIsVisible()}
              onChange={column.getToggleVisibilityHandler()}
            />
            {column.id}
          </label>
        ))}
      </div>
      
      <table>{/* ... */}</table>
    </>
  );
}
```

### CRITICAL: useReactTable Must Complete Before Using Table Methods

```tsx
// ❌ WRONG: Using table methods conditionally
function Table({ data }) {
  if (!data) return <Loading />;
  
  const table = useReactTable({ data, columns, ... });
  // This breaks if the component returns early before useReactTable on some renders
}

// ✅ CORRECT: useReactTable always runs
function Table({ data }) {
  const table = useReactTable({
    data: data ?? [],  // Provide fallback
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (!data) return <Loading />;
  
  // Now safe to use table methods
  return <table>{/* ... */}</table>;
}
```

### Complete Table Example

```tsx
import { useState, useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  flexRender,
  type ColumnDef,
  type SortingState,
  type ColumnFiltersState,
  type PaginationState,
  type VisibilityState,
} from '@tanstack/react-table';

interface DataType {
  id: string;
  name: string;
  status: string;
  value: number;
}

const columns: ColumnDef<DataType>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'value', header: 'Value' },
];

interface TableProps {
  data: DataType[];
  isLoading?: boolean;
}

export function DataTable({ data, isLoading }: TableProps) {
  // ALL STATE HOOKS FIRST
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({});
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 50,
  });

  // TABLE HOOK - always runs with fallback data
  const table = useReactTable({
    data: data ?? [],
    columns,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      pagination,
    },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  // CONDITIONAL RETURNS AFTER ALL HOOKS
  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!data || data.length === 0) {
    return <div>No data available</div>;
  }

  // RENDER
  return (
    <div>
      <table>
        <thead>
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {row.getVisibleCells().map(cell => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div>
        <button
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </button>
        <span>
          Page {table.getState().pagination.pageIndex + 1} of{' '}
          {table.getPageCount()}
        </span>
        <button
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

---

## URL State Management

### useSearchParams (React Router)

```tsx
import { useSearchParams } from 'react-router-dom';

function Component() {
  const [searchParams, setSearchParams] = useSearchParams();

  // Read params
  const page = searchParams.get('page') ?? '1';
  const filter = searchParams.get('filter') ?? '';

  // Update single param (preserves others)
  const updatePage = (newPage: number) => {
    setSearchParams(prev => {
      prev.set('page', String(newPage));
      return prev;
    });
  };

  // Update multiple params
  const updateFilters = (filters: Record<string, string>) => {
    setSearchParams(prev => {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) {
          prev.set(key, value);
        } else {
          prev.delete(key); // Remove empty params
        }
      });
      return prev;
    });
  };

  // Clear all params
  const clearFilters = () => {
    setSearchParams({});
  };
}
```

### Syncing URL with Component State

```tsx
function FilteredTable() {
  const [searchParams, setSearchParams] = useSearchParams();

  // Parse URL params to state
  const filters = useMemo(() => ({
    page: Number(searchParams.get('page') ?? '1'),
    pageSize: Number(searchParams.get('page_size') ?? '50'),
    matched: searchParams.get('matched') === 'true' ? true 
           : searchParams.get('matched') === 'false' ? false 
           : undefined,
    vendorName: searchParams.get('vendor_name') ?? undefined,
    search: searchParams.get('search') ?? '',
  }), [searchParams]);

  // Memoized callback to update URL - CRITICAL for preventing infinite loops
  const updateFilters = useCallback((updates: Partial<typeof filters>) => {
    setSearchParams(prev => {
      Object.entries(updates).forEach(([key, value]) => {
        const paramKey = key.replace(/([A-Z])/g, '_$1').toLowerCase(); // camelCase to snake_case
        if (value !== undefined && value !== '' && value !== null) {
          prev.set(paramKey, String(value));
        } else {
          prev.delete(paramKey);
        }
      });
      return prev;
    });
  }, [setSearchParams]);

  // Use in query
  const { data, isLoading } = useQuery({
    queryKey: ['items', filters],
    queryFn: () => fetchItems(filters),
  });

  return (
    <>
      <Filters
        values={filters}
        onChange={updateFilters} // Stable reference due to useCallback
      />
      <Table data={data?.items} isLoading={isLoading} />
      <Pagination
        page={filters.page}
        pageSize={filters.pageSize}
        total={data?.total ?? 0}
        onPageChange={(page) => updateFilters({ page })}
        onPageSizeChange={(pageSize) => updateFilters({ pageSize, page: 1 })}
      />
    </>
  );
}
```

### CRITICAL: Memoize Callbacks Passed to Children

```tsx
// ❌ WRONG: New function every render - causes infinite loops
function Parent() {
  const [searchParams, setSearchParams] = useSearchParams();

  return (
    <TextFilter
      value={searchParams.get('search') ?? ''}
      onChange={(value) => { // New function every render!
        setSearchParams(prev => {
          prev.set('search', value);
          return prev;
        });
      }}
    />
  );
}

// ✅ CORRECT: Memoized callback
function Parent() {
  const [searchParams, setSearchParams] = useSearchParams();

  const handleSearchChange = useCallback((value: string) => {
    setSearchParams(prev => {
      if (value) {
        prev.set('search', value);
      } else {
        prev.delete('search');
      }
      return prev;
    });
  }, [setSearchParams]); // setSearchParams is stable

  return (
    <TextFilter
      value={searchParams.get('search') ?? ''}
      onChange={handleSearchChange}
    />
  );
}
```

---

## Component Patterns

### Debounced Input

```tsx
import { useState, useEffect, useRef } from 'react';

interface DebouncedInputProps {
  value: string;
  onChange: (value: string) => void;
  debounceMs?: number;
  placeholder?: string;
}

export function DebouncedInput({
  value: externalValue,
  onChange,
  debounceMs = 300,
  placeholder,
}: DebouncedInputProps) {
  const [internalValue, setInternalValue] = useState(externalValue);
  const isFirstRender = useRef(true);

  // Sync from external value only when it actually changes
  // and differs from internal value
  useEffect(() => {
    if (externalValue !== internalValue) {
      setInternalValue(externalValue);
    }
  }, [externalValue]); // Intentionally not including internalValue

  // Debounce internal value changes to external
  useEffect(() => {
    // Skip first render to avoid calling onChange on mount
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }

    const timer = setTimeout(() => {
      if (internalValue !== externalValue) {
        onChange(internalValue);
      }
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [internalValue, debounceMs]); // Intentionally not including onChange, externalValue

  return (
    <input
      value={internalValue}
      onChange={(e) => setInternalValue(e.target.value)}
      placeholder={placeholder}
    />
  );
}
```

### Select Filter

```tsx
interface SelectFilterProps {
  value: string | undefined;
  onChange: (value: string | undefined) => void;
  options: { label: string; value: string }[];
  placeholder?: string;
}

export function SelectFilter({
  value,
  onChange,
  options,
  placeholder = 'All',
}: SelectFilterProps) {
  return (
    <select
      value={value ?? ''}
      onChange={(e) => onChange(e.target.value || undefined)}
    >
      <option value="">{placeholder}</option>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
```

### Boolean Filter (Tri-state)

```tsx
interface BooleanFilterProps {
  value: boolean | undefined;
  onChange: (value: boolean | undefined) => void;
  labels?: { true: string; false: string; all: string };
}

export function BooleanFilter({
  value,
  onChange,
  labels = { true: 'Yes', false: 'No', all: 'All' },
}: BooleanFilterProps) {
  return (
    <select
      value={value === undefined ? '' : String(value)}
      onChange={(e) => {
        const val = e.target.value;
        onChange(val === '' ? undefined : val === 'true');
      }}
    >
      <option value="">{labels.all}</option>
      <option value="true">{labels.true}</option>
      <option value="false">{labels.false}</option>
    </select>
  );
}
```

---

## Common Errors & Fixes

### "Rendered more/fewer hooks than during the previous render"

**Cause:** Hooks called conditionally or after early return.

**Fix:** Move all hooks to top of component, before any conditions.

```tsx
// ❌ Causes error
function Component({ data }) {
  if (!data) return null;
  const [state, setState] = useState(null); // Hook after return
}

// ✅ Fixed
function Component({ data }) {
  const [state, setState] = useState(null); // Hook before return
  if (!data) return null;
}
```

### "Maximum update depth exceeded"

**Cause:** Infinite loop from setState in useEffect.

**Common patterns that cause this:**

```tsx
// ❌ useEffect updates state that's in its own dependencies
useEffect(() => {
  setCount(count + 1);
}, [count]); // count changes, effect runs, sets count, repeat forever

// ❌ Object/array in dependencies creates new reference each render
useEffect(() => {
  doSomething();
}, [{ a: 1 }]); // New object every render

// ❌ Callback prop not memoized
function Parent() {
  return <Child onChange={(x) => setState(x)} />; // New function every render
}
function Child({ onChange }) {
  useEffect(() => {
    onChange(value);
  }, [value, onChange]); // onChange changes every render
}
```

**Fixes:**

```tsx
// ✅ Use functional update
useEffect(() => {
  setCount(prev => prev + 1);
}, []); // No dependency on count

// ✅ Memoize objects
const options = useMemo(() => ({ a: 1 }), []);
useEffect(() => {
  doSomething();
}, [options]);

// ✅ Memoize callbacks
const handleChange = useCallback((x) => setState(x), []);
return <Child onChange={handleChange} />;
```

### "Cannot read properties of undefined (reading 'getAllLeafColumns')"

**Cause:** Using table methods before useReactTable is called.

**Fix:** Ensure useReactTable runs unconditionally.

```tsx
// ❌ Table not initialized on some renders
function Table({ data }) {
  if (!data) return <Loading />;
  const table = useReactTable({ data, columns, ... });
}

// ✅ Table always initialized
function Table({ data }) {
  const table = useReactTable({ 
    data: data ?? [], 
    columns, 
    getCoreRowModel: getCoreRowModel(),
  });
  if (!data) return <Loading />;
}
```

### Query not fetching

**Possible causes:**

1. **`enabled` is false:**
```tsx
// Check your enabled condition
useQuery({
  queryKey: ['data', id],
  queryFn: () => fetch(id),
  enabled: !!id, // Is id actually defined?
});
```

2. **queryKey doesn't include variables:**
```tsx
// ❌ Won't refetch when filters change
useQuery({
  queryKey: ['data'],
  queryFn: () => fetch(filters),
});

// ✅ Refetches when filters change
useQuery({
  queryKey: ['data', filters],
  queryFn: () => fetch(filters),
});
```

3. **Data is cached and still fresh:**
```tsx
// Force refetch
const { refetch } = useQuery({ ... });
refetch();

// Or invalidate cache
const queryClient = useQueryClient();
queryClient.invalidateQueries({ queryKey: ['data'] });
```

### Data loaded but not displayed

**Possible causes:**

1. **Wrong data path:**
```tsx
// API returns { items: [...], total: N }
const { data } = useQuery({ ... });

// ❌ Wrong - data is the whole response
<Table data={data} />

// ✅ Correct - extract items
<Table data={data?.items} />
```

2. **Columns don't match data shape:**
```tsx
// Data has: { name: 'John' }
// ❌ Wrong accessor
{ accessorKey: 'userName', header: 'Name' }

// ✅ Correct accessor
{ accessorKey: 'name', header: 'Name' }
```

---

## Debugging Methodology

### Step 1: Identify the Error

- Check browser console for error messages
- Check React DevTools for component state
- Check Network tab for API requests

### Step 2: Isolate the Problem

```tsx
// Add debug output
console.log('Render', { data, isLoading, isError });

// Or use a debug component
function Debug({ value, label }: { value: unknown; label: string }) {
  return (
    <pre style={{ background: '#f0f0f0', padding: '1rem', fontSize: '12px' }}>
      {label}: {JSON.stringify(value, null, 2)}
    </pre>
  );
}

// Usage
<Debug label="Query State" value={{ isLoading, isError, data: data?.items?.length }} />
```

### Step 3: Check Each Layer

**Routing:**
```tsx
const { runId } = useParams();
console.log('Route params:', { runId });
// Is runId defined? Is it the expected value?
```

**Query:**
```tsx
const query = useQuery({ ... });
console.log('Query state:', {
  status: query.status,
  isLoading: query.isLoading,
  isError: query.isError,
  error: query.error,
  data: query.data,
});
// Is the query running? Did it succeed? What's the data shape?
```

**Data transformation:**
```tsx
console.log('Data for table:', {
  raw: query.data,
  items: query.data?.items,
  itemCount: query.data?.items?.length,
  firstItem: query.data?.items?.[0],
});
// Is items an array? Does it have data?
```

**Table:**
```tsx
console.log('Table state:', {
  rowCount: table.getRowModel().rows.length,
  columnCount: table.getAllColumns().length,
  visibleColumns: table.getVisibleLeafColumns().map(c => c.id),
});
// Are rows being generated? Are columns visible?
```

### Step 4: Network Tab Checklist

1. **Is the request being made?**
   - No → Query not enabled or not triggered
   - Yes → Continue

2. **What's the request URL?**
   - Correct endpoint?
   - Correct query params?
   - snake_case vs camelCase?

3. **What's the response status?**
   - 200 → Check response body
   - 404 → Wrong URL or resource doesn't exist
   - 500 → Backend error

4. **What's the response body?**
   - Does it match expected shape?
   - Is items an array?
   - Are there actually items in the array?

### Step 5: Component Tree Checklist

Using React DevTools:

1. Is the component mounting?
2. What props is it receiving?
3. What's the internal state?
4. Is it re-rendering excessively?

---

## Integration Patterns

### Complete Data Table Page Pattern

```tsx
// types.ts
interface Filters {
  page: number;
  pageSize: number;
  search: string;
  status: string | undefined;
}

// useFilters.ts
function useFilters() {
  const [searchParams, setSearchParams] = useSearchParams();

  const filters: Filters = useMemo(() => ({
    page: Number(searchParams.get('page') ?? '1'),
    pageSize: Number(searchParams.get('page_size') ?? '50'),
    search: searchParams.get('search') ?? '',
    status: searchParams.get('status') ?? undefined,
  }), [searchParams]);

  const setFilters = useCallback((updates: Partial<Filters>) => {
    setSearchParams(prev => {
      Object.entries(updates).forEach(([key, value]) => {
        const paramKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
        if (value !== undefined && value !== '' && value !== null) {
          prev.set(paramKey, String(value));
        } else {
          prev.delete(paramKey);
        }
      });
      // Reset to page 1 when filters change (except page itself)
      if (!('page' in updates)) {
        prev.set('page', '1');
      }
      return prev;
    });
  }, [setSearchParams]);

  const resetFilters = useCallback(() => {
    setSearchParams({});
  }, [setSearchParams]);

  return { filters, setFilters, resetFilters };
}

// useDataQuery.ts
function useDataQuery(filters: Filters) {
  return useQuery({
    queryKey: ['data', filters],
    queryFn: async () => {
      const params = new URLSearchParams({
        page: String(filters.page),
        page_size: String(filters.pageSize),
      });
      if (filters.search) params.set('search', filters.search);
      if (filters.status) params.set('status', filters.status);

      const response = await fetch(`/api/data?${params}`);
      if (!response.ok) throw new Error('Failed to fetch');
      return response.json();
    },
  });
}

// Page.tsx
function DataPage() {
  const { filters, setFilters, resetFilters } = useFilters();
  const { data, isLoading, isError, error } = useDataQuery(filters);

  // Memoized callbacks for filter components
  const handleSearchChange = useCallback(
    (search: string) => setFilters({ search }),
    [setFilters]
  );

  const handleStatusChange = useCallback(
    (status: string | undefined) => setFilters({ status }),
    [setFilters]
  );

  const handlePageChange = useCallback(
    (page: number) => setFilters({ page }),
    [setFilters]
  );

  if (isError) {
    return <ErrorState message={error.message} onRetry={() => window.location.reload()} />;
  }

  return (
    <div>
      <div className="filters">
        <DebouncedInput
          value={filters.search}
          onChange={handleSearchChange}
          placeholder="Search..."
        />
        <SelectFilter
          value={filters.status}
          onChange={handleStatusChange}
          options={statusOptions}
          placeholder="All statuses"
        />
        <button onClick={resetFilters}>Clear filters</button>
      </div>

      <DataTable
        data={data?.items ?? []}
        columns={columns}
        isLoading={isLoading}
      />

      {data && (
        <Pagination
          page={filters.page}
          pageSize={filters.pageSize}
          total={data.total}
          onPageChange={handlePageChange}
        />
      )}
    </div>
  );
}
```

---

## Performance Considerations

### Avoid Unnecessary Re-renders

1. **Memoize expensive computations:**
```tsx
const sortedData = useMemo(
  () => data.sort((a, b) => a.name.localeCompare(b.name)),
  [data]
);
```

2. **Memoize callbacks:**
```tsx
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

3. **Memoize column definitions:**
```tsx
const columns = useMemo(() => [...], [dependencies]);
```

4. **Use React.memo for child components:**
```tsx
const TableRow = React.memo(function TableRow({ row }) {
  return <tr>{/* ... */}</tr>;
});
```

### Large Data Sets

1. **Server-side pagination** - Don't load all data at once
2. **Virtualization** - For 1000+ rows, use @tanstack/react-virtual
3. **Debounce filters** - Don't fetch on every keystroke

---

## Checklist

### Before Implementing

- [ ] All hooks will be at the top of component, before any conditions
- [ ] Column definitions will be stable (outside component or memoized)
- [ ] All callbacks passed to children will use useCallback
- [ ] Query keys will include all variables used in queryFn
- [ ] Query will have proper enabled condition

### After Implementing

- [ ] No console errors or warnings
- [ ] useReactTable called before any table methods
- [ ] Data passed to table is correct shape (items array, not full response)
- [ ] Filters update URL params
- [ ] URL params initialize filter state on page load
- [ ] Loading state displays correctly
- [ ] Empty state displays correctly
- [ ] Error state displays correctly
- [ ] Pagination works
- [ ] Filtering works
- [ ] No infinite loops

### Debugging

- [ ] Check console for errors
- [ ] Check Network tab for requests
- [ ] Add console.log at each layer (route, query, data, table)
- [ ] Verify data shape matches expected
- [ ] Verify column accessors match data keys
- [ ] Check React DevTools for component state
