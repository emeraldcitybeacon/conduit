/**
 * End-to-end test covering inline resource editing and saving.
 *
 * The scenario navigates directly to a known resource, updates the first phone
 * number field, and expects a confirmation toast once the change is saved.
 */
import { test, expect } from '@playwright/test';

test.describe('Resource edit and save', () => {
  test('volunteer edits phone number and saves', async ({ page }) => {
    // Navigate to an existing resource record by ID.
    await page.goto('/pulse/r/00000000-0000-0000-0000-000000000000');

    // Update the first phone number field.
    const phoneInput = page.getByLabel('Phone number').first();
    await phoneInput.fill('555-000-1234');

    // Save changes.
    await page.getByRole('button', { name: 'Save' }).click();

    // Expect a toast message confirming success.
    await expect(page.getByText('Changes saved')).toBeVisible();
  });
});
