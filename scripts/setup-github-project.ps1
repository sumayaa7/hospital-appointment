# Requires token with scopes: repo + project
# https://github.com/settings/tokens -> Generate new token (classic)
# Usage: $env:GITHUB_TOKEN = "ghp_..." ; .\scripts\setup-github-project.ps1

param(
    [string]$Token = $env:GITHUB_TOKEN,
    [string]$Login = "sumayaa7",
    [string]$Repo = "hospital-appointment",
    [int]$ProjectNumber = 1
)

if (-not $Token) {
    Write-Error "Set GITHUB_TOKEN (needs repo + project scopes)."
    exit 1
}

$headers = @{
    Authorization = "Bearer $Token"
    "Content-Type" = "application/json"
}

function Invoke-Gql($query, $variables = @{}) {
    $body = @{ query = $query; variables = $variables } | ConvertTo-Json -Depth 10 -Compress
    $r = Invoke-RestMethod -Uri "https://api.github.com/graphql" -Method Post -Headers $headers -Body $body
    if ($r.errors) {
        throw ($r.errors | ForEach-Object { $_.message } | Out-String)
    }
    return $r
}

$statusOptions = @(
    @{ name = "01 — Idea & scope"; color = "GRAY" },
    @{ name = "02 — Repo & gitignore"; color = "GRAY" },
    @{ name = "03 — Python venv"; color = "BLUE" },
    @{ name = "04 — Flask app factory"; color = "BLUE" },
    @{ name = "05 — Database models"; color = "BLUE" },
    @{ name = "06 — init-db & demo data"; color = "BLUE" },
    @{ name = "07 — Route: index"; color = "BLUE" },
    @{ name = "08 — Route: book"; color = "BLUE" },
    @{ name = "09 — Route: cancel"; color = "BLUE" },
    @{ name = "10 — Route: admin"; color = "BLUE" },
    @{ name = "11 — Jinja2 templates"; color = "PURPLE" },
    @{ name = "12 — CSS & UI"; color = "PURPLE" },
    @{ name = "13 — Team documentation"; color = "PURPLE" },
    @{ name = "14 — Manual test"; color = "YELLOW" },
    @{ name = "15 — Chat: system guide"; color = "ORANGE" },
    @{ name = "16 — Chat: RAG dependencies"; color = "ORANGE" },
    @{ name = "17 — Chat: Ollama models"; color = "ORANGE" },
    @{ name = "18 — Chat: rag_build.py"; color = "ORANGE" },
    @{ name = "19 — Chat: index vectors"; color = "ORANGE" },
    @{ name = "20 — Chat: rag_chat.py"; color = "ORANGE" },
    @{ name = "21 — Chat: POST /chat"; color = "ORANGE" },
    @{ name = "22 — Chat: assistant init"; color = "ORANGE" },
    @{ name = "23 — Chat: widget UI"; color = "ORANGE" },
    @{ name = "24 — Chat: frontend fetch"; color = "ORANGE" },
    @{ name = "25 — Chat: test Q&A"; color = "ORANGE" },
    @{ name = "26 — Presentation ready"; color = "GREEN" },
    @{ name = "Done"; color = "GREEN" }
)

Write-Host "Fetching project..."
$projectQuery = @'
query($login: String!, $number: Int!) {
  user(login: $login) {
    projectV2(number: $number) {
      id
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue { id title }
            ... on DraftIssue { id title }
          }
        }
      }
      fields(first: 30) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options { id name }
          }
        }
      }
    }
  }
}
'@

$proj = Invoke-Gql $projectQuery @{ login = $Login; number = $ProjectNumber }
$project = $proj.data.user.projectV2
$projectId = $project.id
$statusField = $project.fields.nodes | Where-Object { $_.name -eq "Status" } | Select-Object -First 1

Write-Host "Updating Status field options..."
$updateField = @'
mutation($fieldId: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]!) {
  updateProjectV2SingleSelectField(input: { fieldId: $fieldId, singleSelectOptions: $options }) {
    projectV2SingleSelectField { options { id name } }
  }
}
'@
$optInput = $statusOptions | ForEach-Object { @{ name = $_.name; color = $_.color; description = "" } }
$updated = Invoke-Gql $updateField @{ fieldId = $statusField.id; options = $optInput }
$optionMap = @{}
foreach ($o in $updated.data.updateProjectV2SingleSelectField.projectV2SingleSelectField.options) {
    $optionMap[$o.name] = $o.id
}
$doneId = $optionMap["Done"]

$existingTitles = @{}
foreach ($item in $project.items.nodes) {
    if ($item.content.title) { $existingTitles[$item.content.title] = $item.id }
}

Write-Host "Loading issues from repository..."
$issuesQuery = @'
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    issues(states: OPEN, labels: ["project-roadmap"], first: 50) {
      nodes { id number title }
    }
  }
}
'@
$issues = (Invoke-Gql $issuesQuery @{ owner = $Login; name = $Repo }).data.repository.issues.nodes

$addItem = @'
mutation($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: { projectId: $projectId, contentId: $contentId }) {
    item { id }
  }
}
'@

$setStatus = @'
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }
  ) { projectV2Item { id } }
}
'@

foreach ($issue in $issues) {
    $title = $issue.title
    Write-Host "Processing: $title"

    if ($existingTitles.ContainsKey($title)) {
        $itemId = $existingTitles[$title]
    } else {
        $added = Invoke-Gql $addItem @{ projectId = $projectId; contentId = $issue.id }
        $itemId = $added.data.addProjectV2ItemById.item.id
    }

    $statusName = if ($title -match "^26") { "26 — Presentation ready" } else { "Done" }
    $optId = if ($statusName -eq "Done") { $doneId } else { $optionMap[$statusName] }
    if ($optId) {
        Invoke-Gql $setStatus @{
            projectId = $projectId
            itemId = $itemId
            fieldId = $statusField.id
            optionId = $optId
        } | Out-Null
    }
    Start-Sleep -Milliseconds 250
}

Write-Host ""
Write-Host "SUCCESS. Open your board:"
Write-Host "https://github.com/users/$Login/projects/$ProjectNumber"
