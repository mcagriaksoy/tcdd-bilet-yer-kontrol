export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }
  const { from, to, date } = req.body;
  // TODO: Call Selenium backend here and return real results
  res.status(200).json({
    message: "This is a placeholder. Integrate Selenium backend here.",
    from,
    to,
    date,
  });
}
