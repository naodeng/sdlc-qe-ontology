import { expect, test } from '@playwright/test';

test('Chinese overview identifies bundled data and unrun validation', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: '质量证据总览' })).toBeVisible();
  await expect(page.getByText('尚未运行', { exact: true })).toBeVisible();
  await expect(page.getByText('仓库内置示例', { exact: true })).toBeVisible();

  await page.getByRole('menuitem', { name: '数据导入' }).click();
  await expect(page.getByRole('heading', { name: '导入项目数据' })).toBeVisible();
  await expect(page.getByText(/导入流程尚未实现/)).toBeVisible();
  await expect(page.getByText('首个导入格式：受限 JSON（输入 profile 另行定义）')).toBeVisible();
});

test('language switch presents the English copy on request', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'EN' }).click();

  await expect(page.getByRole('heading', { name: 'Quality evidence overview' })).toBeVisible();
  await expect(page.getByRole('menuitem', { name: 'Import data' })).toBeVisible();
});
