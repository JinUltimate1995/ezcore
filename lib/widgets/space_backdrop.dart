import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// The studio-plate backdrop: a planet limb at the bottom edge, layered
/// mountain silhouettes, drifting nebula wash, twinkling stars and an
/// occasional meteor.
///
/// Two layers, on purpose:
///
/// * [SpaceScenePainter] paints the expensive geometry — gradients, the
///   planet, the ridges — exactly once.
/// * [StarfieldPainter] repaints on every animation frame, but it only
///   draws ~120 tiny circles and one streak, so it stays cheap.
///
/// Motion is optional. When the `motion` setting is off, or the OS asks
/// for reduced motion, the controller never ticks: no frames are
/// scheduled and the scene holds still at `t = 0`.
class SpaceBackdrop extends StatefulWidget {
  const SpaceBackdrop({super.key, this.motion = true});

  /// Mirrors the user's "Ambient motion" preference.
  final bool motion;

  @override
  State<SpaceBackdrop> createState() => _SpaceBackdropState();
}

class _SpaceBackdropState extends State<SpaceBackdrop>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  bool _reduced = false;
  bool _animating = false;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      // One full cycle of twinkle + a single meteor pass.
      duration: const Duration(seconds: 24),
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _reduced = MediaQuery.disableAnimationsOf(context);
    // Always reconcile, not only when the flag changes: the very first
    // call has to start the animation too.
    _sync();
  }

  @override
  void didUpdateWidget(SpaceBackdrop old) {
    super.didUpdateWidget(old);
    if (widget.motion != old.motion) _sync();
  }

  void _sync() {
    final shouldRun = widget.motion && !_reduced;
    if (shouldRun == _animating) return;
    _animating = shouldRun;
    if (shouldRun) {
      _ctrl.repeat();
    } else {
      _ctrl.stop();
      _ctrl.value = 0;
    }
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      child: Stack(
        fit: StackFit.expand,
        children: [
          const RepaintBoundary(
            child: CustomPaint(painter: SpaceScenePainter()),
          ),
          RepaintBoundary(
            child: AnimatedBuilder(
              // A stopped controller never notifies, so this layer costs
              // nothing while motion is off.
              animation: _ctrl,
              builder: (context, _) => CustomPaint(
                painter: StarfieldPainter(t: _ctrl.value),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/// A star: normalised position, size, brightness tier and twinkle phase.
class _Star {
  const _Star(this.x, this.y, this.r, this.tier, this.phase);
  final double x;
  final double y;
  final double r;
  final int tier;
  final double phase;
}

/// Deterministic star field — generated once, identical on every launch
/// and on every device, so the sky never reshuffles itself on rebuild.
final List<_Star> _sky = _buildSky();

List<_Star> _buildSky() {
  // Fixed-seed LCG: a plain `Random()` would differ per run and make the
  // backdrop look different every launch.
  var seed = 0x1F2E3D4C;
  double next() {
    seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF;
    return seed / 0x7FFFFFFF;
  }

  final out = <_Star>[];
  for (var i = 0; i < 140; i++) {
    // Bias stars toward the top: the planet fills the lower band.
    final y = math.pow(next(), 1.5).toDouble();
    final tierRoll = next();
    final tier = tierRoll > 0.93 ? 2 : (tierRoll > 0.7 ? 1 : 0);
    final r = switch (tier) { 2 => 1.5 + next() * 0.7, 1 => 0.9 + next() * 0.5, _ => 0.5 + next() * 0.35 };
    out.add(_Star(next(), y, r, tier, next() * math.pi * 2));
  }
  return out;
}

/// Static half of the scene: sky, nebula, planet limb, ridges, vignette.
class SpaceScenePainter extends CustomPainter {
  const SpaceScenePainter();

  @override
  void paint(Canvas canvas, Size size) {
    if (size.isEmpty) return;
    final w = size.width;
    final h = size.height;

    // --- Sky: deep zenith into a slightly warmer mid field.
    canvas.drawRect(
      Offset.zero & size,
      Paint()
        ..shader = const LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Tokens.spaceDeep, Tokens.spaceMid, Tokens.spaceDeep],
          stops: [0.0, 0.55, 1.0],
        ).createShader(Offset.zero & size),
    );

    // --- Nebula wash: two soft clouds, the scene's only large soft fill.
    _wash(
      canvas,
      size,
      center: Alignment(w * 0.78, h * 0.12),
      radius: math.max(w, h) * 0.72,
      color: Tokens.spaceNebula.withValues(alpha: 0.55),
    );
    _wash(
      canvas,
      size,
      center: Alignment(w * 0.12, h * 0.34),
      radius: math.max(w, h) * 0.55,
      color: const Color(0xFF0B1B33).withValues(alpha: 0.6),
    );

    // --- Ringed companion planet, top right (the plate's second body).
    _companionPlanet(canvas, size);

    // --- Main planet limb across the lower edge.
    _planet(canvas, size);

    // --- Two mountain silhouettes anchor the frame bottom.
    _ridge(canvas, size, far: true);
    _ridge(canvas, size, far: false);

    // --- Vignette keeps the UI legible over the scene.
    canvas.drawRect(
      Offset.zero & size,
      Paint()
        ..shader = RadialGradient(
          center: Alignment.center,
          radius: 0.95,
          colors: [Colors.transparent, Tokens.bg.withValues(alpha: 0.55)],
          stops: const [0.55, 1.0],
        ).createShader(Offset.zero & size),
    );
  }

  void _wash(
    Canvas canvas,
    Size size, {
    required Alignment center,
    required double radius,
    required Color color,
  }) {
    final paint = Paint()
      ..shader = RadialGradient(
        colors: [color, Colors.transparent],
        stops: const [0.0, 1.0],
      ).createShader(
        Rect.fromCircle(
          center: center.withinRect(Offset.zero & size),
          radius: radius,
        ),
      );
    canvas.drawRect(Offset.zero & size, paint);
  }

  void _companionPlanet(Canvas canvas, Size size) {
    // Small and dim on purpose: it is a distant body, not a UI element.
    // Anything larger competes with the search field in the top corner.
    final unit = math.min(size.width, size.height);
    final c = Offset(size.width * 0.90, size.height * 0.07);
    final r = unit * 0.085;
    const fade = 0.55;

    // Body: dark disc with a lit upper-left edge.
    canvas.drawCircle(
      c,
      r,
      Paint()
        ..color = Colors.black.withValues(alpha: 0.0)
        ..shader = LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            const Color(0xFF17345C).withValues(alpha: fade),
            const Color(0xFF060A12).withValues(alpha: fade),
          ],
        ).createShader(Rect.fromCircle(center: c, radius: r)),
    );
    // Atmosphere rim.
    canvas.drawCircle(
      c,
      r,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.2
        ..color = Tokens.planetRim.withValues(alpha: 0.30)
        ..shader = LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Tokens.planetRimHi.withValues(alpha: 0.45),
            Tokens.planetRim.withValues(alpha: 0.25),
            Colors.transparent,
          ],
        ).createShader(Rect.fromCircle(center: c, radius: r * 1.2)),
    );
    // Ring: a thin ellipse crossing the disc, the plate's signature detail.
    final ring = Rect.fromCenter(
      center: c,
      width: r * 2.9,
      height: r * 0.72,
    );
    canvas.save();
    canvas.translate(c.dx, c.dy);
    canvas.rotate(-0.32);
    canvas.translate(-c.dx, -c.dy);
    canvas.drawOval(
      ring,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.0
        ..color = Tokens.planetRim.withValues(alpha: 0.24),
    );
    canvas.restore();
  }


  void _planet(Canvas canvas, Size size) {
    // Centre sits below the frame so only the limb's crown is visible.
    final c = Offset(size.width * 0.42, size.height * 1.62);
    final r = size.height * 1.18;
    final disc = Rect.fromCircle(center: c, radius: r);

    // Body.
    canvas.drawCircle(
      c,
      r,
      Paint()
        ..shader = LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [const Color(0xFF12233C), Tokens.planetBody],
          stops: const [0.0, 0.45],
        ).createShader(disc),
    );

    // Atmospheric halo: wide and soft, the glow that sells the limb.
    canvas.drawCircle(
      c,
      r,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = r * 0.055
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 26)
        ..color = Tokens.planetRim.withValues(alpha: 0.30),
    );
    // Inner rim light.
    canvas.drawCircle(
      c,
      r,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2.2
        ..shader = LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Tokens.planetRimHi, Tokens.planetRim, Colors.transparent],
          stops: const [0.0, 0.35, 0.9],
        ).createShader(disc),
    );
  }

  void _ridge(Canvas canvas, Size size, {required bool far}) {
    final h = size.height;
    final baseY = far ? h * 0.94 : h * 1.02;
    final amp = far ? h * 0.10 : h * 0.14;
    // Fixed phases: far ridge peaks are higher and wider, near ridge jagged.
    final peaks = far
        ? const [0.0, 0.14, 0.23, 0.36, 0.5, 0.63, 0.78, 0.9, 1.0]
        : const [0.0, 0.08, 0.17, 0.28, 0.41, 0.52, 0.66, 0.8, 0.92, 1.0];
    final heights = far
        ? const [0.0, 0.55, 0.32, 0.78, 0.45, 0.68, 0.35, 0.6, 0.0]
        : const [0.0, 0.7, 0.42, 0.95, 0.5, 0.8, 0.38, 0.72, 0.55, 0.0];

    final path = Path()..moveTo(0, size.height);
    for (var i = 0; i < peaks.length; i++) {
      final x = peaks[i] * size.width;
      final y = baseY - heights[i] * amp;
      if (i == 0) {
        path.lineTo(x, y);
      } else {
        final prevX = peaks[i - 1] * size.width;
        final prevY = baseY - heights[i - 1] * amp;
        // Control point above the midpoint: soft mountain shoulders.
        final midX = (prevX + x) / 2;
        final midY = math.min(prevY, y) - amp * 0.12;
        path.quadraticBezierTo(midX, midY, x, y);
      }
    }
    path
      ..lineTo(size.width, size.height)
      ..close();

    canvas.drawPath(
      path,
      Paint()
        ..color = far ? Tokens.ridgeFar : Tokens.ridgeNear
        ..style = PaintingStyle.fill,
    );

    // Moonlit edge along the crest of the near ridge.
    if (!far) {
      canvas.drawPath(
        path,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1.0
          ..color = Tokens.planetRim.withValues(alpha: 0.22),
      );
    }
  }

  @override
  bool shouldRepaint(SpaceScenePainter oldDelegate) => false;
}

/// Animated half of the scene: star twinkle plus one meteor per cycle.
class StarfieldPainter extends CustomPainter {
  const StarfieldPainter({required this.t});

  /// Animation position in `0..1`.
  final double t;

  @override
  void paint(Canvas canvas, Size size) {
    if (size.isEmpty) return;
    // Minimum scale factor: a 0-width window would otherwise draw stars
    // stacked on the same pixel.
    final unit = math.min(size.width, size.height) / 800;
    for (final s in _sky) {
      // Gentle twinkle: each star breathes on its own phase.
      final tw = 0.55 + 0.45 * math.sin((t * math.pi * 2) + s.phase);
      final paint = Paint()
        ..color = (s.tier == 2 ? Tokens.starHi : Tokens.starDim)
            .withValues(alpha: (s.tier == 2 ? 0.95 : 0.55) * tw)
        ..maskFilter = s.tier == 2 && unit > 0.6
            ? const MaskFilter.blur(BlurStyle.normal, 1.4)
            : null;
      canvas.drawCircle(
        Offset(s.x * size.width, s.y * size.height),
        s.r * math.max(unit, 0.45),
        paint,
      );
    }
    _meteor(canvas, size);
  }

  /// A single streak early in each 24s cycle, so the sky is never static
  /// but never busy.
  void _meteor(Canvas canvas, Size size) {
    const flight = 0.055; // fraction of the cycle the streak is visible
    if (t >= flight) return;
    final k = t / flight;
    // Ease-out travel from the upper right toward the lower left.
    final start = Offset(size.width * 0.78, size.height * 0.04);
    final travel = Offset(-size.width * 0.34, size.height * 0.30);
    final pos = start + travel * (1 - math.pow(1 - k, 3).toDouble());
    final fade = (1 - k) * (k < 0.12 ? k / 0.12 : 1);

    canvas.drawLine(
      pos,
      pos + const Offset(54, 42),
      Paint()
        ..strokeWidth = 1.6
        ..strokeCap = StrokeCap.round
        ..color = Tokens.planetRimHi.withValues(alpha: 0.55 * fade),
    );
    canvas.drawLine(
      pos,
      pos + const Offset(18, 14),
      Paint()
        ..strokeWidth = 2.4
        ..strokeCap = StrokeCap.round
        ..color = Colors.white.withValues(alpha: 0.75 * fade),
    );
  }

  @override
  bool shouldRepaint(StarfieldPainter oldDelegate) => oldDelegate.t != t;
}
