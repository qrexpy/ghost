import discord

# Cheers Nes for the method!
async def get_external_asset(bot, asset_url, app_id):
    if not asset_url or asset_url == "":
        return None
    if not asset_url.startswith("https://"):
        return asset_url
    assets = await bot.http.request(discord.http.Route("POST", f"/applications/{app_id}/external-assets"), json={"urls": [asset_url]})
    for asset in assets:
        return f"mp:{str(asset['external_asset_path'])}"
    
def parse_external_asset(asset_url):
    if asset_url.startswith("mp:"):
        return "https://" + asset_url.split("/https/")[1]
    
    return asset_url if asset_url else None

def generate_activity_json(cfg_rpc, external_assets):
    activity_json = {
        "name": cfg_rpc.get("name", "Ghost"),
        "type": 0,  # ActivityType.playing
        "application_id": str(cfg_rpc.get("client_id")),
        "state": cfg_rpc.get("state", None),
        "details": cfg_rpc.get("details", None),
        "assets": {
            "large_image": external_assets["large_image"],
            "large_text": cfg_rpc.get("large_text", None),
            "small_image": external_assets["small_image"],
            "small_text": cfg_rpc.get("small_text", None)
        }
    }
    
    # loop through each key in activity, if its value is empty, set it to None
    for key, value in activity_json.items():
        if isinstance(value, str) and not value:
            activity_json[key] = None
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, str) and not sub_value:
                    value[sub_key] = None
                    
    return activity_json