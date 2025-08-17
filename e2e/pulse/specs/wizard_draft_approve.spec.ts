/**
 * End-to-end test for the creation wizard and subsequent draft approval flow.
 *
 * The test walks through the three-step wizard to create a draft resource and
 * then simulates an editor approving the draft from the review list.
 */
import { test, expect } from '@playwright/test';

test.describe('Wizard create and approve', () => {
  test('editor approves a draft created via wizard', async ({ page }) => {
    // Start the wizard.
    await page.goto('/pulse/new');

    // Step 1: Organization details.
    await page.getByLabel('Organization Name').fill('Playwright Test Org');
    await page.getByRole('button', { name: 'Next' }).click();

    // Step 2: Location details.
    await page.getByLabel('Street').fill('123 Test St');
    await page.getByLabel('City').fill('Testville');
    await page.getByRole('button', { name: 'Next' }).click();

    // Step 3: Service details.
    await page.getByLabel('Service Name').fill('Testing Service');
    await page.getByRole('button', { name: 'Review' }).click();

    // Submit draft for approval.
    await page.getByRole('button', { name: 'Submit Draft' }).click();

    // Navigate to the draft review list and approve the draft.
    await page.goto('/pulse/review/drafts');
    await page.getByText('Playwright Test Org').click();
    await page.getByRole('button', { name: 'Approve' }).click();

    // Confirm the draft was approved.
    await expect(page.getByText('Draft approved')).toBeVisible();
  });
});
