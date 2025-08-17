/**
 * Playwright configuration for Pulse end-to-end tests.
 *
 * The configuration uses a single Chromium browser profile and points to the
 * development server running on localhost. The `E2E_BASE_URL` environment
 * variable can override the default when running against a deployed instance.
 */
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './specs',
  /* Increase the timeout slightly to accommodate slower CI environments. */
  timeout: 30 * 1000,
  use: {
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:8000',
    headless: true,
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
