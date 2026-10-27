// Mor: wash the playing cover's colour faintly over the violet background. The colour comes
// from Spotify's own extracted-colours query (Spicetify.colorExtractor returns null since 1.2.9x).
(function morCoverTint() {
  const GQL = window.Spicetify?.GraphQL;
  if (!Spicetify?.Player?.addEventListener || !GQL?.Definitions?.fetchExtractedColors) {
    setTimeout(morCoverTint, 500);
    return;
  }
  const apply = async () => {
    const md = Spicetify.Player.data?.item?.metadata;
    const image = (md?.image_xlarge_url || md?.image_url || "").replace("spotify:image:", "https://i.scdn.co/image/");
    if (!image) { setTimeout(apply, 1000); return; }  // player data comes after the page
    try {
      const r = await GQL.Request(GQL.Definitions.fetchExtractedColors, { imageUris: [image] });
      const hex = r?.data?.extractedColors?.[0]?.colorDark?.hex;
      if (hex) document.documentElement.style.setProperty("--cover-tint", hex + "40");
    } catch (e) { /* keep the last tint */ }
  };
  Spicetify.Player.addEventListener("songchange", apply);
  apply();
})();
