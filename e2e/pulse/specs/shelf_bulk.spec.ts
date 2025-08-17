/**
 * End-to-end test for shelf-based bulk operations.
 *
 * The test adds two resources to the shelf, stages a phone number update,
 * previews the changes, commits them, and finally exercises the undo path.
 */
import { test, expect } from '@playwright/test';

test.describe('Shelf bulk apply', () => {
  test('stage, preview, commit and undo a bulk phone update', async ({ page }) => {
    // Add first resource to the shelf.
    await page.goto('/pulse/r/00000000-0000-0000-0000-000000000000');
    await page.getByRole('button', { name: 'Add to shelf' }).click();

    // Add second resource to the shelf.
    await page.goto('/pulse/r/00000000-0000-0000-0000-000000000001');
    await page.getByRole('button', { name: 'Add to shelf' }).click();

    // Open the shelf drawer and start a bulk edit.
    await page.getByRole('button', { name: 'Shelf' }).click();
    await page.getByRole('button', { name: 'Bulk edit' }).click();

    // Stage a phone number change.
    await page.getByLabel('Phone number').fill('555-000-9999');
    await page.getByRole('button', { name: 'Preview' }).click();

    // Commit the change.
    await page.getByRole('button', { name: 'Commit' }).click();
    await expect(page.getByText('Bulk operation applied')).toBeVisible();

    // Undo the operation.
    await page.getByRole('button', { name: 'Undo' }).click();
    await expect(page.getByText('Bulk operation undone')).toBeVisible();
  });
});
