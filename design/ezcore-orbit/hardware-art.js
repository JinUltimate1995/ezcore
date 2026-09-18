(function (global) {
  'use strict';

  // === Color Palette ===
  var S = '#DDE6F4', SL = '#EAF0FB', SD = '#B0BFD8', SH = '#7A8AA0';
  var K = '#0A0A0A', KL = '#1E1E2E', KD = '#050508';
  var B = '#007BFF', BL = '#4DA3FF', BD = '#005BBF';
  var GR = '#6B7B8F', GRL = '#8896A8';

  // === ID-safe unique suffix generator ===
  function uid(core, sfx) {
    return 'ha_' + core.replace(/[^a-z0-9]/gi, '_') + '_' + sfx;
  }

  // === SVG scaffolding ===
  function open(label) {
    return '<svg class="hardware-art" viewBox="0 0 320 240" role="img" aria-label="' + label + '" xmlns="http://www.w3.org/2000/svg">';
  }
  function close() { return '</svg>'; }

  // === Shape helpers ===
  function lg(id, y1, y2, c0, c1) {
    return '<linearGradient id="' + id + '" x1="0%" y1="' + y1 + '%" x2="0%" y2="' + y2 + '%"><stop offset="0%" stop-color="' + c0 + '"/><stop offset="100%" stop-color="' + c1 + '"/></linearGradient>';
  }
  function r(x, y, w, h, fill, rx, stroke, sw) {
    var a = rx != null ? ' rx="' + rx + '"' : '';
    var b = stroke ? ' stroke="' + stroke + '" stroke-width="' + (sw || 1) + '"' : '';
    return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '"' + a + ' fill="' + fill + '"' + b + '/>';
  }
  function c(cx, cy, rd, fill, stroke) {
    var a = stroke ? ' stroke="' + stroke + '" stroke-width="1"' : '';
    return '<circle cx="' + cx + '" cy="' + cy + '" r="' + rd + '" fill="' + fill + '"' + a + '/>';
  }
  function e(cx, cy, rx, ry, fill, stroke) {
    var a = stroke ? ' stroke="' + stroke + '" stroke-width="1"' : '';
    return '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + ry + '" fill="' + fill + '"' + a + '/>';
  }
  function p(pts, fill, stroke) {
    var a = stroke ? ' stroke="' + stroke + '" stroke-width="1"' : '';
    return '<polygon points="' + pts + '" fill="' + fill + '"' + a + '/>';
  }
  function path(d, fill, stroke) {
    var a = stroke ? ' stroke="' + stroke + '" stroke-width="1" fill="none"' : ' fill="' + fill + '"';
    return '<path d="' + d + '"' + a + '/>';
  }
  function screen(x, y, w, h, rx) {
    var rr = rx || 4;
    return '<g>' + r(x, y, w, h, K, rr) + r(x + 3, y + 3, w - 6, h - 6, BD, rr - 1) + r(x + 6, y + 6, w - 12, h - 12, B, rr - 2) + '</g>';
  }
  function dpad(cx, cy, w, h) {
    return '<g>' + r(cx - w * 1.4, cy - h * 0.4, w * 2.8, h * 0.8, KL, 2) + r(cx - h * 0.4, cy - w * 1.4, h * 0.8, w * 2.8, KL, 2) + '</g>';
  }
  function pill(x, y, w, h, fill) {
    return r(x, y, w, h, fill, h / 2);
  }
  function led(cx, cy, r, color) {
    return '<g>' + c(cx, cy, r, color) + c(cx - r * 0.3, cy - r * 0.3, r * 0.4, '#fff', null, 'opacity:0.6') + '</g>';
  }

  // =============================================
  //  RENDERERS — one per hardware silhouette
  // =============================================

  // ── Game Boy (sameboy / gambatte) ──────────
  function gb(id) {
    var d = lg(uid(id, 'bg'), 0, 100, SL, SD);
    var s = open('Game Boy original portrait handheld');
    s += '<defs>' + d + '</defs>';
    // Main body
    s += r(100, 30, 120, 250, 'url(#' + uid(id, 'bg') + ')', 18, SH, 2);
    s += r(100, 30, 120, 12, SL, 10);
    // Screen bezel + screen
    s += r(114, 52, 92, 88, K, 8);
    s += r(118, 56, 84, 80, BD, 5);
    s += r(122, 60, 76, 72, B, 4);
    s += '<line x1="126" y1="64" x2="155" y2="64" stroke="' + BL + '" stroke-width="1.5" opacity="0.55"/>';
    // Power LED
    s += led(128, 158, 4, '#FF4444');
    // D-Pad
    s += dpad(138, 190, 22, 8);
    // A / B buttons
    s += c(184, 195, 13, K); s += c(184, 195, 10, KL); s += c(184, 195, 4, '#222236');
    s += c(158, 212, 13, K); s += c(158, 212, 10, KL); s += c(158, 212, 4, '#222236');
    // Start / Select pills
    s += pill(128, 242, 34, 10, KL);
    s += pill(128, 242, 30, 7, '#222236');
    s += pill(185, 242, 34, 10, KL);
    s += pill(185, 242, 30, 7, '#222236');
    // Speaker grille
    for (var i = 0; i < 6; i++) {
      s += '<line x1="' + (158 + i * 7) + '" y1="260" x2="' + (158 + i * 7) + '" y2="274" stroke="' + KL + '" stroke-width="2.5" stroke-linecap="round"/>';
    }
    s += close();
    return s;
  }

  // ── Game Boy Advance (mgba) — wide with side grips ──
  function gba(id) {
    var d = lg(uid(id, 'bg'), 0, 100, SL, SD);
    var s = open('Game Boy Advance landscape handheld with side grips');
    s += '<defs>' + d + '</defs>';
    // Center body
    s += r(30, 70, 260, 110, 'url(#' + uid(id, 'bg') + ')', 12, SH, 2);
    // Left grip (bulbous)
    s += r(15, 80, 50, 90, S, 20, SH, 1);
    s += r(15, 80, 50, 90, 'url(#' + uid(id, 'bg') + ')', 20);
    // Right grip
    s += r(255, 80, 50, 90, S, 20, SH, 1);
    s += r(255, 80, 50, 90, 'url(#' + uid(id, 'bg') + ')', 20);
    // Screen
    s += r(110, 80, 100, 70, K, 5);
    s += r(114, 84, 92, 62, BD, 3);
    s += r(118, 88, 84, 54, B, 2);
    // D-pad on left grip
    s += dpad(55, 110, 14, 6);
    // A/B on right grip
    s += c(268, 100, 9, K); s += c(268, 100, 7, KL);
    s += c(282, 115, 9, K); s += c(282, 115, 7, KL);
    // Shoulder buttons L/R
    s += r(30, 65, 40, 12, KL, 4, SH, 1);
    s += r(250, 65, 40, 12, KL, 4, SH, 1);
    // Start / Select
    s += pill(145, 158, 24, 8, KL);
    s += pill(178, 158, 24, 8, KL);
    // Power LED
    s += led(200, 75, 2.5, '#44FF44');
    s += close();
    return s;
  }

  // ── NES (mesen) — front-loading rectangular deck ──
  function nes(id) {
    var d = lg(uid(id, 'bg'), 0, 100, SL, '#9AACB8');
    var s = open('Nintendo Entertainment System front-loading deck');
    s += '<defs>' + d + '</defs>';
    // Top deck surface (grey)
    s += r(30, 80, 260, 70, 'url(#' + uid(id, 'bg') + ')', 4, SH, 2);
    // Ribbed top texture lines
    for (var i = 0; i < 8; i++) {
      s += '<line x1="' + (40 + i * 30) + '" y1="82" x2="' + (40 + i * 30) + '" y2="110" stroke="#B0BCC8" stroke-width="1" opacity="0.5"/>';
    }
    // Front dark flap (cartridge loader)
    s += r(80, 150, 160, 35, K, 3, SH, 1);
    s += r(85, 153, 150, 12, KL, 2);
    // Eject lever
    s += r(140, 170, 40, 10, GR, 3, SH, 1);
    // Controller ports
    s += r(100, 125, 20, 8, KD, 1);
    s += r(200, 125, 20, 8, KD, 1);
    // Power LED (blue)
    s += led(95, 142, 3, B);
    // Dark stripe between top and front
    s += r(80, 148, 160, 4, KD);
    // Cartridge slot (black)
    s += r(140, 152, 30, 8, K, 1);
    s += close();
    return s;
  }

  // ── SNES (snes9x) — rounded deck ──
  function snes(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#D8DDE8', '#98A4B8');
    var s = open('Super Nintendo rounded deck');
    s += '<defs>' + d + '</defs>';
    // Rounded body
    s += r(35, 75, 250, 90, 'url(#' + uid(id, 'bg') + ')', 16, SH, 2);
    // Cartridge slot on top
    s += r(120, 72, 80, 12, KL, 3, SH, 1);
    // Cartridge slot (black)
    s += r(130, 68, 60, 10, K, 2, SH, 1);
    // Eject / Power buttons (blue)
    s += r(80, 105, 30, 14, '#8B6F9B', 3, SH, 1);
    s += r(120, 105, 30, 14, '#8B6F9B', 3, SH, 1);
    s += r(80, 105, 30, 14, BD, 3);
    s += r(120, 105, 30, 14, BD, 3);
    // Reset button
    s += c(250, 112, 5, KL); s += c(250, 112, 3, '#2A2A3A');
    // Power LED (blue)
    s += led(75, 112, 3, B);
    // Controller ports
    s += r(145, 135, 14, 7, KD, 1);
    s += r(165, 135, 14, 7, KD, 1);
    // Slider switches on top edge
    s += r(200, 76, 20, 6, KL, 2);
    s += r(225, 76, 20, 6, KL, 2);
    s += close();
    return s;
  }

  // ── N64 (mupen64plus) — 3-prong controller + console ──
  function n64(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#DCDDE4', '#A8ADB8');
    var s = open('Nintendo 64 three-prong controller and console');
    s += '<defs>' + d + '</defs>';
    // Console (small box at bottom)
    s += r(40, 200, 100, 28, 'url(#' + uid(id, 'bg') + ')', 3, SH, 1);
    s += r(44, 203, 20, 6, KL, 1);
    s += led(130, 210, 2.5, B);
    // Controller — 3-prong Y shape via polygons
    // Main body (center prong top section)
    s += r(175, 80, 60, 50, S, 8, SH, 1);
    // Left prong
    s += p('155,130 200,130 185,195 145,195', S, SH);
    // Right prong
    s += p('235,130 210,130 220,195 250,195', S, SH);
    // Bottom prong (joystick holder)
    s += p('185,180 220,180 230,140 175,140', S, SH);
    // Analog stick
    s += c(200, 120, 12, K); s += c(200, 120, 9, KL); s += c(200, 120, 3, B);
    // D-pad on left prong
    s += dpad(160, 160, 10, 4);
    // A button (blue-ish circle)
    s += c(220, 95, 11, K); s += c(220, 95, 8, BD);
    // B button
    s += c(240, 105, 9, K); s += c(240, 105, 7, '#4A2A2A');
    // C buttons
    s += c(215, 70, 5, B, SH, 1);
    s += c(230, 65, 5, B, SH, 1);
    s += c(245, 70, 5, B, SH, 1);
    // Z trigger
    s += r(190, 195, 30, 8, KL, 3, SH, 1);
    // Power LED
    s += led(200, 205, 3, B);
    s += close();
    return s;
  }

  // ── DS (melonds) — open clamshell ──
  function ds(id) {
    var d = lg(uid(id, 'bg'), 0, 100, SL, SD);
    var s = open('Nintendo DS open clamshell with two screens');
    s += '<defs>' + d + '</defs>';
    // Bottom half (main controls)
    s += r(60, 140, 200, 85, 'url(#' + uid(id, 'bg') + ')', 8, SH, 2);
    // Top half (screen only)
    s += r(60, 20, 200, 110, S, 8, SH, 2);
    // Hinge
    s += r(130, 128, 60, 14, KL, 3, SH, 1);
    // Top screen
    s += r(78, 32, 164, 80, K, 4);
    s += r(82, 36, 156, 72, BD, 3);
    s += r(86, 40, 148, 64, B, 2);
    // Bottom screen (touch)
    s += r(78, 152, 164, 60, K, 4);
    s += r(82, 156, 156, 52, '#1A2A4A', 3);
    s += r(86, 160, 148, 44, B, 2);
    s += '<text x="160" y="188" text-anchor="middle" fill="' + BL + '" font-size="7" font-family="monospace" opacity="0.7">TOUCH</text>';
    // D-pad on bottom left
    s += dpad(108, 195, 8, 3);
    // Buttons on bottom right
    s += c(215, 188, 6, K); s += c(215, 188, 4, '#3A2020');
    s += c(228, 200, 6, K); s += c(228, 200, 4, '#20203A');
    s += c(202, 200, 6, K); s += c(202, 200, 4, '#203A20');
    s += c(215, 212, 6, K); s += c(215, 212, 4, '#3A3A20');
    // Start/Select
    s += pill(148, 222, 18, 6, KL);
    s += pill(172, 222, 18, 6, KL);
    // Mic hole
    s += c(160, 235, 3, KD);
    // Power LED
    s += led(90, 25, 2, '#44FF44');
    s += close();
    return s;
  }

  // ── Dolphin — GameCube cube + slim Wii ──
  function dolphin(id) {
    var dg = lg(uid(id, 'gc'), 0, 100, '#B8B8CC', '#808098');
    var dw = lg(uid(id, 'wi'), 0, 100, '#E8ECF0', '#C0C8D0');
    var s = open('Nintendo GameCube cube and slim Wii console');
    s += '<defs>' + dg + dw + '</defs>';
    // GameCube body (cube)
    s += r(40, 100, 100, 100, 'url(#' + uid(id, 'gc') + ')', 4, SH, 2);
    // Disc lid on top (circle)
    s += c(90, 100, 40, '#9090A8', SH);
    s += c(90, 100, 35, '#A8A8BC');
    s += c(90, 100, 10, '#7878A0');
    // Handle on back (top edge arc)
    s += '<path d="M 50,100 Q 90,75 130,100" stroke="' + SH + '" stroke-width="2" fill="none"/>';
    // Controller ports on front
    s += r(60, 160, 12, 6, K, 1);
    s += r(78, 160, 12, 6, K, 1);
    s += r(96, 160, 12, 6, K, 1);
    s += r(114, 160, 12, 6, K, 1);
    // Power button (black)
    s += c(90, 140, 8, K); s += c(90, 140, 5, '#2A2A3A');
    // Reset
    s += c(108, 140, 4, K);
    // Wii (slim rectangle to the right)
    s += r(190, 120, 100, 60, 'url(#' + uid(id, 'wi') + ')', 6, SH, 2);
    // Wii disc slot
    s += r(195, 145, 90, 8, KL, 2);
    // Wii ports
    s += r(200, 160, 14, 6, KD, 1);
    s += r(220, 160, 14, 6, KD, 1);
    // Wii power LED (blue)
    s += led(275, 130, 3, B);
    // GameCube power button blue accent
    s += c(90, 140, 5, B);
    // Stand base for Wii
    s += r(185, 180, 110, 8, '#B0B8C4', 2, SH, 1);
    s += close();
    return s;
  }

  // ── PlayStation (swanstation) — circular disc lid ──
  function ps1(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#D8DCE4', '#A0A8B4');
    var s = open('Original PlayStation with circular disc lid');
    s += '<defs>' + d + '</defs>';
    // Main body (slightly taller at back)
    s += r(50, 90, 220, 70, 'url(#' + uid(id, 'bg') + ')', 6, SH, 2);
    // Circular disc lid (ellipse from front angle)
    s += e(160, 88, 80, 18, '#C0C8D4', SH);
    s += e(160, 88, 70, 14, '#B0B8C8');
    s += e(160, 88, 30, 5, '#98A0B0');
    // Lid seam line
    s += '<line x1="80" y1="100" x2="240" y2="100" stroke="' + SH + '" stroke-width="1.5"/>';
    // Power button (blue)
    s += r(100, 110, 22, 10, BD, 3, SH, 1);
    // Eject button (black)
    s += r(130, 110, 22, 10, KL, 3, SH, 1);
    // Controller ports (black)
    s += r(165, 110, 16, 8, K, 2);
    s += r(187, 110, 16, 8, K, 2);
    // Parallel port (top right)
    s += r(220, 95, 30, 8, '#5A5A6A', 1, SH, 1);
    // Reset button (black)
    s += c(210, 115, 3, K);
    // LED (blue)
    s += led(90, 115, 2.5, B);
    s += close();
    return s;
  }

  // ── PSP (ppsspp) — wide black handheld ──
  function psp(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#2A2A30', '#0A0A0E');
    var s = open('PlayStation Portable wide black handheld');
    s += '<defs>' + d + '</defs>';
    // Main body
    s += r(20, 60, 280, 120, 'url(#' + uid(id, 'bg') + ')', 10, '#333340', 2);
    // Central large screen
    s += r(95, 72, 130, 86, K, 5);
    s += r(100, 77, 120, 76, BD, 3);
    s += r(104, 81, 112, 68, B, 2);
    // D-pad left
    s += dpad(65, 120, 12, 5);
    // Action buttons right
    s += c(255, 105, 7, '#888898'); s += c(255, 105, 5, '#AAAAB8');
    s += c(268, 118, 7, '#888898'); s += c(268, 118, 5, '#AAAAB8');
    s += c(242, 118, 7, '#888898'); s += c(242, 118, 5, '#AAAAB8');
    s += c(255, 131, 7, '#888898'); s += c(255, 131, 5, '#AAAAB8');
    // Analog nub
    s += c(70, 150, 8, '#333340'); s += c(70, 150, 5, '#444455');
    // Shoulder buttons
    s += r(30, 55, 35, 10, '#1A1A22', 3, '#333340', 1);
    s += r(255, 55, 35, 10, '#1A1A22', 3, '#333340', 1);
    // Start / Select / Home
    s += pill(140, 158, 18, 6, '#333340');
    s += pill(165, 158, 18, 6, '#333340');
    s += c(190, 161, 5, '#333340');
    s += close();
    return s;
  }

  // ── Mega Drive (genesis_plus_gx) — oval deck with cartridge slot ──
  function md(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#D4D4DC', '#9098A4');
    var s = open('Sega Mega Drive oval deck with cartridge slot');
    s += '<defs>' + d + '</defs>';
    // Main oval body
    s += r(40, 80, 240, 80, 'url(#' + uid(id, 'bg') + ')', 12, SH, 2);
    // Cartridge slot on top (black)
    s += r(135, 72, 50, 14, K, 2, SH, 1);
    s += r(138, 74, 44, 3, KL);
    // Top extension (oval cap)
    s += e(160, 80, 120, 14, S, SH);
    // Power slider
    s += r(70, 100, 22, 10, K, 3, SH, 1);
    s += r(72, 102, 18, 6, '#2A2A3A', 2);
    // Reset button
    s += c(105, 105, 6, K); s += c(105, 105, 4, '#2A2A3A');
    // Volume slider
    s += r(210, 100, 30, 6, KL, 2);
    s += r(220, 101, 8, 4, '#4A4A5A', 1);
    // Controller ports (black)
    s += r(110, 130, 14, 6, K, 1);
    s += r(130, 130, 14, 6, K, 1);
    s += r(150, 130, 14, 6, K, 1);
    // LED (blue)
    s += led(70, 125, 3, B);
    s += close();
    return s;
  }

  // ── Saturn (beetle_saturn) — circular lid deck ──
  function saturn(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#E0E2E8', '#B0B4C0');
    var s = open('Sega Saturn circular lid deck');
    s += '<defs>' + d + '</defs>';
    // Main body (slightly rounded rectangle)
    s += r(50, 95, 220, 70, 'url(#' + uid(id, 'bg') + ')', 8, SH, 2);
    // Circular disc lid on top
    s += e(160, 92, 75, 16, '#C8CCD4', SH);
    s += e(160, 92, 65, 12, '#B8BCC8');
    s += e(160, 92, 25, 5, '#A0A4B0');
    // Lid opening seam
    s += '<line x1="85" y1="105" x2="235" y2="105" stroke="' + SH + '" stroke-width="1.5"/>';
    // Power button (round, black)
    s += c(100, 120, 9, K, SH, 1);
    s += c(100, 120, 6, '#3A3A4A');
    s += c(100, 120, 2, '#5A5A6A');
    // Eject button (blue)
    s += r(130, 117, 24, 10, BD, 3, SH, 1);
    // Controller ports (2 ports visible, black)
    s += r(170, 130, 14, 6, K, 1);
    s += r(190, 130, 14, 6, K, 1);
    // LED (blue)
    s += led(80, 120, 3, B);
    s += close();
    return s;
  }

  // ── Dreamcast (flycast) — square lid with four front ports ──
  function dreamcast(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#D8DAE0', '#A8ACB4');
    var s = open('Sega Dreamcast square disc lid with four front controller ports');
    s += '<defs>' + d + '</defs>';
    // Main body (slightly tapered)
    s += r(60, 90, 200, 75, 'url(#' + uid(id, 'bg') + ')', 6, SH, 2);
    // Square disc lid on top
    s += r(110, 78, 100, 20, '#B8BCC4', 4, SH, 1);
    s += r(115, 80, 90, 16, '#A8ACB4', 3);
    s += r(125, 83, 70, 10, '#989CA8', 2);
    // Opening seam
    s += '<line x1="70" y1="105" x2="250" y2="105" stroke="' + SH + '" stroke-width="1.5"/>';
    // Power / Eject (black)
    s += r(90, 110, 28, 10, K, 3, SH, 1);
    s += r(128, 110, 28, 10, K, 3, SH, 1);
    // Four controller ports (front, black)
    s += r(168, 125, 12, 6, K, 1);
    s += r(186, 125, 12, 6, K, 1);
    s += r(204, 125, 12, 6, K, 1);
    s += r(222, 125, 12, 6, K, 1);
    // VMU slots (small windows above ports, black)
    s += r(168, 118, 12, 4, K, 1);
    s += r(186, 118, 12, 4, K, 1);
    s += r(204, 118, 12, 4, K, 1);
    s += r(222, 118, 12, 4, K, 1);
    // LED / speed dial (blue)
    s += led(80, 115, 3, B);
    s += close();
    return s;
  }

  // ── PC Engine (beetle_pce) — small square deck ──
  function pce(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#E0E4EA', '#B0B8C4');
    var s = open('PC Engine small square deck');
    s += '<defs>' + d + '</defs>';
    // Compact main body
    s += r(100, 85, 120, 80, 'url(#' + uid(id, 'bg') + ')', 4, SH, 2);
    // Cartridge slot (black)
    s += r(140, 78, 40, 12, K, 2, SH, 1);
    // Top ridge detail
    s += '<line x1="105" y1="88" x2="215" y2="88" stroke="' + SH + '" stroke-width="1"/>';
    // Power button (black)
    s += c(125, 115, 6, K, SH, 1);
    s += c(125, 115, 3, '#3A3A4A');
    // Reset button (black)
    s += c(145, 115, 4, K);
    // Controller port (black)
    s += r(170, 112, 16, 7, K, 2);
    // LED (blue)
    s += led(115, 135, 2.5, B);
    // HuCard slot detail
    s += r(130, 140, 60, 8, '#5A5A6A', 1, SH, 1);
    s += close();
    return s;
  }

  // ── Atari 2600 (stella) — wedge with ridges ──
  function atari(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#C0C0C0', '#808080');
    var s = open('Atari 2600 wedge console with ridged top');
    s += '<defs>' + d + '</defs>';
    // Wider front, wedge profile
    s += p('50,170 270,170 260,80 60,80', 'url(#' + uid(id, 'bg') + ')', SH);
    // Ridges on top
    for (var i = 0; i < 7; i++) {
      s += '<line x1="' + (70 + i * 28) + '" y1="90" x2="' + (60 + i * 28) + '" y2="170" stroke="#A0A0A0" stroke-width="2"/>';
    }
    for (var i = 0; i < 7; i++) {
      s += '<line x1="' + (70 + i * 28) + '" y1="90" x2="' + (60 + i * 28) + '" y2="170" stroke="#D0D0D0" stroke-width="1" opacity="0.5"/>';
    }
    // Black front stripe with switches
    s += r(65, 135, 190, 30, K, 0);
    // Difficulty switches
    s += r(80, 142, 14, 10, '#3A3A3A', 2);
    s += r(100, 142, 14, 10, '#3A3A3A', 2);
    // Game select / reset
    s += r(140, 144, 20, 6, '#4A4A4A', 1);
    s += r(168, 144, 20, 6, '#4A4A4A', 1);
    // Power LED (blue)
    s += led(220, 150, 3, B);
    // Controller port (back top)
    s += r(70, 82, 20, 5, '#5A5A5A', 1);
    s += r(100, 82, 20, 5, '#5A5A5A', 1);
    s += r(130, 82, 20, 5, '#5A5A5A', 1);
    s += r(160, 82, 20, 5, '#5A5A5A', 1);
    s += r(190, 82, 20, 5, '#5A5A5A', 1);
    s += r(220, 82, 20, 5, '#5A5A5A', 1);
    s += close();
    return s;
  }

  // ── Arcade (fbneo) — cabinet ──
  function arcade(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#D0D4DC', '#9098A8');
    var s = open('Arcade cabinet');
    s += '<defs>' + d + '</defs>';
    // Cabinet body (tall)
    s += r(100, 20, 120, 220, 'url(#' + uid(id, 'bg') + ')', 4, SH, 2);
    // Marquee at top
    s += r(105, 24, 110, 30, K, 3);
    s += r(110, 28, 100, 22, '#2A1A3A', 2);
    s += '<text x="160" y="43" text-anchor="middle" fill="' + BL + '" font-size="8" font-family="monospace" font-weight="bold" opacity="0.9">INSERT COIN</text>';
    // Screen
    s += r(108, 58, 104, 80, K, 4);
    s += r(112, 62, 96, 72, BD, 3);
    s += r(116, 66, 88, 64, B, 2);
    // Bezel frame
    s += r(106, 56, 108, 84, 'none', 4, KL, 2);
    // Control panel (angled section)
    s += r(95, 148, 130, 40, S, 3, SH, 1);
    // Joystick base
    s += c(140, 165, 10, K); s += c(140, 165, 7, KL); s += c(140, 165, 3, '#4A4A5A');
    // Joystick shaft
    s += r(138, 150, 4, 15, '#888', 1);
    s += c(140, 148, 5, '#CC3333');
    // Buttons
    s += c(175, 160, 6, '#CC3333', K, 1);
    s += c(190, 160, 6, '#3333CC', K, 1);
    s += c(205, 160, 6, '#33CC33', K, 1);
    s += c(175, 178, 6, '#CCCC33', K, 1);
    s += c(190, 178, 6, '#CC33CC', K, 1);
    // Coin slot area
    s += r(110, 195, 20, 12, KL, 2, SH, 1);
    s += r(190, 195, 20, 12, KL, 2, SH, 1);
    // Tray bottom
    s += r(100, 230, 120, 8, SD, 2, SH, 1);
    s += close();
    return s;
  }

  // ── DOSBox (dosbox_pure) — CRT + PC tower ──
  function dosbox(id) {
    var dc = lg(uid(id, 'crt'), 0, 100, '#C0C4CC', '#88909C');
    var dt = lg(uid(id, 'twr'), 0, 100, '#B8BCC4', '#7A8290');
    var s = open('CRT monitor and PC tower');
    s += '<defs>' + dc + dt + '</defs>';
    // CRT monitor body
    s += r(30, 30, 140, 120, 'url(#' + uid(id, 'crt') + ')', 10, SH, 2);
    // CRT screen (slightly curved via inset)
    s += r(40, 40, 120, 90, K, 6);
    s += r(44, 44, 112, 82, '#1A1A2A', 4);
    // Screen text (DOS prompt)
    s += '<text x="52" y="60" fill="#AAAAAA" font-size="7" font-family="monospace">C:\\&gt;dir</text>';
    s += '<text x="52" y="72" fill="#AAAAAA" font-size="6" font-family="monospace"> Volume in</text>';
    s += '<text x="52" y="84" fill="#CCCCCC" font-size="6" font-family="monospace">DOSBOX EXE</text>';
    s += '<text x="52" y="96" fill="#AAAAAA" font-size="6" font-family="monospace">COMMAND COM</text>';
    s += '<text x="52" y="110" fill="#AAAAAA" font-size="7" font-family="monospace">C:\\&gt;_</text>';
    // CRT bezel details
    s += r(80, 135, 20, 6, '#4A4A5A', 2);
    // Power LED on CRT (blue)
    s += led(100, 142, 3, B);
    // PC Tower (to the right)
    s += r(200, 50, 70, 170, 'url(#' + uid(id, 'twr') + ')', 3, SH, 2);
    // 5.25" drive bay
    s += r(208, 65, 54, 12, K, 2, SH, 1);
    s += r(210, 67, 50, 8, '#2A2A34', 1);
    // Floppy slot line
    s += '<line x1="212" y1="73" x2="256" y2="73" stroke="#1A1A22" stroke-width="1"/>';
    // 3.5" drive bay
    s += r(208, 85, 54, 10, K, 2, SH, 1);
    s += r(210, 87, 20, 6, '#2A2A34', 1);
    // Power button on tower
    s += c(235, 120, 7, '#4A4A5A', SH, 1);
    s += c(235, 120, 4, '#3A3A4A');
    // LED on tower (blue)
    s += led(235, 135, 2.5, B);
    // Vent slots on tower
    for (var i = 0; i < 4; i++) {
      s += r(210, 148 + i * 10, 50, 3, '#6A7078', 1);
    }
    // Rear fan
    s += c(235, 210, 8, K, SH);
    s += c(235, 210, 6, '#3A3A44');
    s += close();
    return s;
  }

  // ── ScummVM (scummvm) — CRT adventure engine ──
  function scummvm(id) {
    var d = lg(uid(id, 'bg'), 0, 100, '#C8CCD4', '#8A90A0');
    var s = open('ScummVM adventure game engine on CRT display');
    s += '<defs>' + d + '</defs>';
    // CRT monitor
    s += r(50, 20, 220, 150, 'url(#' + uid(id, 'bg') + ')', 12, SH, 2);
    // Screen
    s += r(62, 32, 196, 110, K, 6);
    s += r(66, 36, 188, 102, '#1A1A2A', 4);
    // Adventure game scene: pixel art room background
    s += r(66, 36, 188, 70, '#1A0A2A', 0); // sky
    s += r(66, 106, 188, 32, '#0A2A0A', 0); // ground
    // Simple pixel character
    s += r(148, 80, 12, 16, '#AA8855', 2); // body
    s += c(154, 76, 5, '#DDBB88'); // head
    s += r(144, 78, 4, 10, '#886644'); // arm
    s += r(160, 78, 4, 10, '#886644'); // arm
    s += r(150, 96, 4, 10, '#553322'); // leg
    s += r(156, 96, 4, 10, '#553322'); // leg
    // Text parser input line at bottom
    s += r(70, 116, 180, 20, K, 0);
    s += '<text x="76" y="130" fill="#CCCCCC" font-size="8" font-family="monospace">&gt; open door_</text>';
    // Verb panel on screen
    s += r(70, 40, 50, 50, 'rgba(0,0,0,0.6)', 3);
    s += '<text x="80" y="52" fill="#FFFFFF" font-size="6" font-family="sans-serif">Open</text>';
    s += '<text x="80" y="62" fill="#FFFFFF" font-size="6" font-family="sans-serif">Close</text>';
    s += '<text x="80" y="72" fill="#FFFFFF" font-size="6" font-family="sans-serif">Give</text>';
    s += '<text x="80" y="82" fill="#FFFFFF" font-size="6" font-family="sans-serif">Pick up</text>';
    // Monitor brand area
    s += r(130, 155, 60, 8, '#4A4A5A', 2);
    s += led(230, 158, 3, B);
    // Blue accent line on screen
    s += r(70, 116, 180, 2, B, 0);
    // Keyboard below
    s += r(60, 180, 200, 30, '#B0B4BC', 3, SH, 1);
    // Key rows
    for (var i = 0; i < 12; i++) {
      s += r(68 + i * 15, 185, 12, 8, '#D0D4D8', 1, '#90949C', 0.5);
    }
    for (var i = 0; i < 11; i++) {
      s += r(75 + i * 15, 196, 12, 8, '#D0D4D8', 1, '#90949C', 0.5);
    }
    // Spacebar
    s += r(110, 206, 80, 6, '#D0D4D8', 1, '#90949C', 0.5);
    s += close();
    return s;
  }

  // =============================================
  //  CORE → RENDERER MAP
  // =============================================
  var RENDERERS = {
    sameboy: gb,
    gambatte: gb,
    mgba: gba,
    mesen: nes,
    snes9x: snes,
    mupen64plus: n64,
    melonds: ds,
    dolphin: dolphin,
    swanstation: ps1,
    ppsspp: psp,
    genesis_plus_gx: md,
    beetle_saturn: saturn,
    flycast: dreamcast,
    beetle_pce: pce,
    stella: atari,
    fbneo: arcade,
    dosbox_pure: dosbox,
    scummvm: scummvm
  };

  // =============================================
  //  PUBLIC API
  // =============================================
  global.hardwareArt = function (coreId) {
    var fn = RENDERERS[coreId];
    if (typeof fn === 'function') return fn(coreId);
    return open(coreId + ' hardware') + r(80, 80, 160, 80, S, 8, SH, 2) +
      '<text x="160" y="125" text-anchor="middle" fill="' + BL + '" font-size="10" font-family="sans-serif">' + coreId + '</text>' + close();
  };

  // Expose renderer count for debugging
  global.hardwareArt.count = Object.keys(RENDERERS).length;

})(typeof window !== 'undefined' ? window : globalThis);
