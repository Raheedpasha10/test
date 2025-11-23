export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Content-Type', 'application/json');

  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).json({ message: 'OK' });
  }

  // Health check
  return res.status(200).json({
    status: 'healthy',
    groq_available: !!process.env.GROQ_API_KEY,
    google_ai_available: !!process.env.GOOGLE_GENAI_API_KEY
  });
}