export default function handler(request, response) {
  response.setHeader('Access-Control-Allow-Origin', '*');
  response.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  response.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (request.method === 'OPTIONS') {
    return response.status(200).end();
  }
  
  return response.status(200).json({
    status: 'healthy',
    groq_available: !!process.env.GROQ_API_KEY,
    timestamp: new Date().toISOString()
  });
}