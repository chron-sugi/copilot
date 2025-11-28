
```
src/
  app/
    router/
      routes.ts
    providers/
      QueryClientProvider.tsx
  features/
    cart/
      components/
        CartPanel/
          CartPanel.tsx
          CartPanel.test.tsx
          CartPanel.module.css
      hooks/
        useCart.ts
        useCart.test.ts
      api/
        get-cart.ts
        update-cart.ts
      model/
        cart.types.ts
        cart.schema.ts   // runtime validation (zod/valibot)
        cart.selectors.ts
      services/
        cart.service.ts  // orchestration over api + model
      index.ts           // named re-exports for the feature
  shared/
    ui/
      Button/
        Button.tsx
        Button.test.tsx
    lib/
      http/
        http-client.ts
      logger/
        logger.ts
    config/
      env.ts
```