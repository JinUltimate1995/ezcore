import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ezcore/services/cover_art.dart';
import 'package:ezcore/services/local_data_dir.dart';
import 'package:ezcore/widgets/orbit_widgets.dart';

void main() {
  final onePixelPng = base64Decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=',
  );

  test('cover spec is deterministic per game id', () {
    final a = coverSpecFor('imp-test-rom');
    final b = coverSpecFor('imp-test-rom');
    expect(a.top, b.top);
    expect(a.bottom, b.bottom);
    expect(a.motif, b.motif);
    expect(a.accent, b.accent);
  });

  test('cover spec stays inside the approved identity ranges', () {
    for (final id in ['a', 'zelda', 'mario-kart-64', 'imp-xyz', 'homebrew']) {
      final spec = coverSpecFor(id);
      expect(spec.motif, inInclusiveRange(0, 4));
      expect(
        [
          spec.top,
          spec.bottom,
        ].every((c) => c >= 0xFF0A0A0A && c <= 0xFF2A3542),
        isTrue,
        reason: 'palette must stay dark navy/slate for $id',
      );
    }
  });

  test('different games spread across palettes and motifs', () {
    final ids = List.generate(24, (i) => 'game-$i');
    final tops = ids.map((id) => coverSpecFor(id).top).toSet();
    final motifs = ids.map((id) => coverSpecFor(id).motif).toSet();
    expect(tops.length, greaterThan(1));
    expect(motifs.length, greaterThan(1));
  });

  test('no pinned screenshot cover resolves to null', () {
    expect(coverFileFor('definitely-not-a-real-game-id-12345'), isNull);
  });

  test('cached cover lookup refreshes after a screenshot is pinned', () {
    final dir = Directory.systemTemp.createTempSync('ezcore-cover-cache-');
    addTearDown(() => dir.deleteSync(recursive: true));
    PlatformLocalDataDirProvider.pinStartupDir(dir.path);
    const id = 'cover-cache-test';
    final art = File('${dir.path}/art/$id.png');

    invalidateCoverFile(id);
    expect(coverFileFor(id), isNull);
    art.parent.createSync(recursive: true);
    art.writeAsBytesSync(onePixelPng);
    expect(coverFileFor(id), isNull, reason: 'the cache avoids disk churn');

    invalidateCoverFile(id);
    expect(coverFileFor(id)?.path, art.path);
  });

  testWidgets('a mounted cover refreshes after a screenshot is pinned', (
    tester,
  ) async {
    final dir = Directory.systemTemp.createTempSync('ezcore-cover-widget-');
    addTearDown(() => dir.deleteSync(recursive: true));
    PlatformLocalDataDirProvider.pinStartupDir(dir.path);
    const id = 'cover-widget-test';
    final art = File('${dir.path}/art/$id.png');
    invalidateCoverFile(id);

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: GameCover(
            gameId: id,
            title: 'Fixture',
            system: 'test',
            width: 120,
            height: 160,
          ),
        ),
      ),
    );
    await tester.pump();
    expect(find.byType(Image), findsNothing);

    art.parent.createSync(recursive: true);
    art.writeAsBytesSync(onePixelPng);
    invalidateCoverFile(id);
    await tester.pump();

    expect(find.byType(Image), findsOneWidget);
  });
}
