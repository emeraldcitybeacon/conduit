/**
 * End-to-end test verifying sensitive resources show redacted data to volunteers.
 *
 * The test navigates to a resource that has been flagged as sensitive and
 * asserts that address and contact details are redacted while a banner warns the
 * user about the sensitive status.
 */
import { test, expect } from '@playwright/test';

test.describe('Sensitive mode redaction', () => {
  test('volunteer views redacted information for sensitive resource', async ({ page }) => {
    // Navigate to a sensitive resource.
    await page.goto('/pulse/r/00000000-0000-0000-0000-000000000002');

    // The sensitive banner should be visible.
    await expect(page.getByText('Sensitive resource')).toBeVisible();

    // Address and contact details should display redaction notices.
    await expect(page.getByText('Address hidden')).toBeVisible();
    await expect(page.getByText('Contact redacted')).toBeVisible();
  });
});
