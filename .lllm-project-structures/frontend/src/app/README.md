# `src/app/` — Application Shell & Composition Root

This folder owns the global app shell, routing, and providers. It **composes** feature modules from `src/features/*` but should not contain domain-specific business logic.

## Folder Structure

```text
src/
  app/
    App.tsx                  # Root application component (used by main.tsx)

    routes/                  # App routing configuration & router setup
      router.tsx             # Creates the router instance (e.g. React Router)
      route-config.ts        # Route definitions → maps paths to feature pages
      guards.ts              # (Optional) route guards, auth checks

    layout/                  # Global layout & chrome
      AppShell.tsx           # Main layout: header/sidebar/content frame
      Header.tsx             # Top navigation bar
      Sidebar.tsx            # Navigation, feature links, filters, etc.
      Footer.tsx             # (Optional) footer
      ErrorBoundary.tsx      # Catch & display UI errors at app-shell level
      LoadingScreen.tsx      # Fallback while routes/features are loading

    providers/               # Global context/providers for the whole app
      AppProviders.tsx       # Wraps children with all providers below
      ThemeProvider.tsx      # Theme, color mode, design system tokens
      QueryClientProvider.tsx# React Query / data-fetching client
      StoreProvider.tsx      # Global store (Redux/Zustand/etc.)
      IntlProvider.tsx       # (Optional) i18n provider

    config/                  # App-level, framework-agnostic configuration
      app.config.ts          # App name, links, feature flags, etc.
      env.config.ts          # Safe, runtime-checked env access
      routes.config.ts       # Central route name ↔ path mappings (if needed)

    hooks/                   # App-wide hooks (not feature-specific)
      useAppInit.ts          # One-time app initialization logic
      useAppTheme.ts         # Read/change current theme
      useRouteChange.ts      # Listen to route change events (analytics, etc.)

    store/                   # App-wide state that crosses many features
      app.store.ts           # Layout state, global flags, “current org”, etc.
      app.selectors.ts       # Derived values from app store

    assets/                  # Global assets referenced by the app shell
      styles/
        index.css            # Global CSS entry (resets, base styles)
        theme.css            # Theme tokens, CSS variables
      icons/
        index.ts             # Central exports for SVG/icon components
      images/
        logo.png
        og-image.png

