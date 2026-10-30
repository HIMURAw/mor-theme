
// Cam: an Apple Music style living backdrop. The playing cover, huge and heavily blurred, drifts
// slowly behind the clear glass panels; a new song crossfades in. Only the cam theme gets this.
(function camBackdrop() {
  if (!document.body || !Spicetify?.Player?.addEventListener) { setTimeout(camBackdrop, 300); return; }
  const host = document.createElement("div");
  host.id = "cam-backdrop";
  host.innerHTML = '<div class="cam-art"></div><div class="cam-art"></div><div class="cam-veil"></div>';
  document.body.prepend(host);
  const layers = host.querySelectorAll(".cam-art");
  let front = 0, last = "";
  const set = () => {
    const md = Spicetify.Player.data?.item?.metadata;
    const url = (md?.image_xlarge_url || md?.image_large_url || md?.image_url || "").replace("spotify:image:", "https://i.scdn.co/image/");
    if (!url) { setTimeout(set, 1000); return; }
    if (url === last) return;
    last = url;
    const img = new Image();
    img.onload = () => {
      front ^= 1;
      layers[front].style.backgroundImage = `url("${url}")`;
      layers[front].classList.add("on");
      layers[front ^ 1].classList.remove("on");
    };
    img.src = url;
  };
  Spicetify.Player.addEventListener("songchange", set);
  set();
})();
