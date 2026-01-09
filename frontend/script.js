function cleanSummary(text) {
  return text
    .replace(/\*\*/g, "")
    .replace(/^\s*[\*\-]\s?/gm, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

async function analyzeChat() {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("status");
  const result = document.getElementById("result");
  const summary = document.getElementById("summary");

  if (!fileInput.files.length) {
    status.innerText = "Please select a WhatsApp .txt or .zip file.";
    return;
  }

  const file = fileInput.files[0];
  const ext = file.name.split(".").pop().toLowerCase();

  if (ext !== "txt" && ext !== "zip") {
    status.innerText = "Only WhatsApp .txt or .zip files are supported.";
    return;
  }

  status.innerText = "Analyzing chat… please wait.";
  result.classList.add("hidden");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData
    });

    // 🔥 IMPORTANT FIX
    const text = await response.text();

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      status.innerText = "Invalid response from backend.";
      return;
    }

    if (!response.ok) {
      status.innerText = data.detail || "Backend error occurred.";
      return;
    }

    summary.innerText = cleanSummary(data.summary);
    result.classList.remove("hidden");
    status.innerText = "Summary generated successfully.";

  } catch (error) {
    status.innerText = "Frontend error: " + error.message;
  }
}
