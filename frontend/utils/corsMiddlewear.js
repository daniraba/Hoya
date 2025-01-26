export const corsMiddleware = async (req, next) => {
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*', // Allow all origins (use specific origin for production)
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    // Handle OPTIONS preflight request
    if (req.method === 'OPTIONS') {
        return new Response(null, {
            status: 204,
            headers: corsHeaders,
        });
    }

    // Pass the request to the next handler
    const response = await next(req);

    // Add CORS headers to the response
    Object.entries(corsHeaders).forEach(([key, value]) => {
        response.headers.set(key, value);
    });

    return response;
};