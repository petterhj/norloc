export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

export function createResponse(response, status) {
  return new Response(JSON.stringify(response), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    status,
  });
}