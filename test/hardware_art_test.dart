import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:ezcore/widgets/hardware_art.dart';

void main() {
  const activeCoreIds = {
    'pocketbit',
    'gambatte',
    'advancebit',
    'nesbyte',
    'superfx',
    'blastproc',
    'joystick',
    'realmode',
    'cardcon',
    'geometry1',
    'rcp64',
    'dualscreen',
    'portcomp',
    'dreamarc',
    'powercube',
    'twinsh',
    'coinbox',
    'pointclick',
  };

  test('active catalog cores have original artwork assets', () {
    final registry =
        jsonDecode(File('cores/registry.json').readAsStringSync())
            as Map<String, dynamic>;
    final active = (registry['cores'] as List)
        .map((id) => id.toString())
        .where((id) => !id.endsWith('_hold'))
        .toSet();

    expect(active, activeCoreIds);
    for (final id in active) {
      final artwork = hardwareArtworkAsset(id);
      expect(artwork, 'assets/core_art/$id.webp', reason: id);
      expect(File(artwork).existsSync(), isTrue, reason: '$id artwork exists');
    }
  });

  test('new cores use system-family artwork without a per-core image', () {
    expect(
      hardwareArtworkAsset('future-pocket-core', systems: ['gba']),
      'assets/core_art/advancebit.webp',
    );
    expect(
      hardwareArtworkAsset('future-dual-screen-core', systems: ['3ds']),
      'assets/core_art/dualscreen.webp',
    );
    expect(
      hardwareArtworkAsset('future-arcade-core', systems: ['neogeo']),
      'assets/core_art/coinbox.webp',
    );
    expect(
      hardwareArtworkAsset('future-pc-core', systems: ['dos']),
      'assets/core_art/realmode.webp',
    );
    expect(
      hardwareArtworkAsset('future-home-computer-core', systems: ['msx']),
      'assets/core_art/realmode.webp',
    );
    expect(
      hardwareArtworkAsset('citra_hold', systems: ['3ds']),
      'assets/core_art/dualscreen.webp',
    );
    expect(
      hardwareArtworkAsset('unknown-core'),
      'assets/core_art/generic.webp',
    );
  });
}
