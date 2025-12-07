# Feature-Sliced Design (FSD) – Project Structure Guide

This project uses **Feature-Sliced Design (FSD)** with the full **7-layer** layout:

> `app → processes → pages → widgets → features → entities → shared`

Each layer organizes code by **responsibility & scope**, and each slice within layers is further split into **segments** by technical purpose.

---

## 1. Top-Level Layout

```text
src/
  app/         # App shell: bootstrapping, routing, global providers, global styles
  pages/       # Route-level pages (compositions of widgets/features/entities)
  widgets/     # Reusable, composite UI blocks used on multiple pages
  features/    # User-facing capabilities (actions that bring business value)
  entities/    # Domain entities (User, Device, OS, Product, etc.)
  shared/      # Generic, domain-agnostic building blocks (UI kit, hooks, infra, libs)
  test/        # Cross-cutting test setup (Jest/Vitest/Playwright, MSW, etc.)
  types/       # Global TypeScript declarations (if needed)

main.tsx # Entrypoint
