// supabase/functions/set-default-role/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
serve(async (req)=>{
  const { record } = await req.json();
  // Call Admin API to update app_metadata
  const res = await fetch(`https://blqtfxldzdxzsfmtafzi.supabase.co/auth/v1/admin/users/${record.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "apikey": Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"),
      "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`
    },
    body: JSON.stringify({
      app_metadata: {
        roles: [
          "student"
        ]
      }
    })
  });
  return new Response(JSON.stringify(await res.json()), {
    status: res.status
  });
});
