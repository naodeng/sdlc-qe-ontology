import { expect, test } from '@playwright/test';

test('creates_lists_and_opens_an_empty_workspace_without_relabeling_demo_data', async ({ page }) => {
  await page.goto('/workspaces');

  await expect(page.getByRole('heading', { name: '工作区', exact: true })).toBeVisible();
  await page.getByLabel('工作区名称').fill('本地回归项目');
  await page.getByRole('button', { name: '创建工作区' }).click();

  await expect(page.getByRole('heading', { name: '本地回归项目' })).toBeVisible();
  await expect(page.getByText('暂无导入数据', { exact: true })).toBeVisible();
  await expect(page.getByText('无活动快照', { exact: true })).toBeVisible();
  await expect(page.locator('.workspace-summary')).toContainText('仓库示例 · 只读');

  await page.getByRole('link', { name: '返回工作区' }).click();
  await page.reload();
  await expect(page.getByRole('heading', { name: '工作区', exact: true })).toBeVisible();
  await page.getByRole('link', { name: '本地回归项目' }).click();
  await expect(page.getByText('暂无导入数据', { exact: true })).toBeVisible();

  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('link', { name: '项目总览' }).click();
  await expect(page.getByRole('heading', { name: '质量证据总览' })).toBeVisible();
  await expect(page.getByText('仓库内置示例', { exact: true })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});
