const { Octokit } = require("@octokit/rest");
const fs = require("fs");

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

async function generateReleaseContent()
{
    const { data: release } = await octokit.repos.getRelease({
        owner: process.env.GITHUB_REPOSITORY.split('/')[0],
        repo: process.env.GITHUB_REPOSITORY.split('/')[1],
        release_id: process.env.GITHUB_EVENT.release.id,
    });

    let content = `# ${release.name}\n\n`;
    content += release.body + "\n\n";

    content += "## Downloads\n\n";
    content += "| Platform | Download | Size | Date |\n";
    content += "|----------|----------|------|------|\n";

    const mainAssets = release.assets.filter(asset =>
        !asset.name.includes("debug") && !asset.name.includes("symbols")
    );

    for (const asset of mainAssets)
    {
        const platform = getPlatformFromAsset(asset.name);
        const size = formatSize(asset.size);
        const date = formatDate(new Date(asset.created_at));
        content += `| ${platform} | [${asset.name}](${asset.browser_download_url}) | ${size} | ${date} |\n`;
    }

    content += "\n## Additional Files\n\n";
    const additionalAssets = release.assets.filter(asset =>
        asset.name.includes("debug") || asset.name.includes("symbols")
    );

    for (const asset of additionalAssets)
    {
        const size = formatSize(asset.size);
        const date = formatDate(new Date(asset.created_at));
        content += `- [${asset.name}](${asset.browser_download_url}) (${size}, ${date})\n`;
    }

    fs.writeFileSync("release-body.md", content);
}

function getPlatformFromAsset(assetName)
{
    if (assetName.includes("windows")) return "Windows";
    if (assetName.includes("macos")) return "macOS";
    if (assetName.includes("linux")) return "Linux";
    return "Other";
}

function formatSize(bytes)
{
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1)
    {
        size /= 1024;
        unitIndex++;
    }

    return `${size.toFixed(1)}${units[unitIndex]}`;
}

function formatDate(date)
{
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0)
    {
        return "Today";
    } else if (diffDays === 1)
    {
        return "Yesterday";
    } else if (diffDays <= 7)
    {
        return `${diffDays} days ago`;
    } else
    {
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
}

generateReleaseContent().catch(console.error);