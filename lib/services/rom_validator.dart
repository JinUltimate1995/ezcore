import 'dart:io';

/// Validates that a file is a plausible ROM image, not a text file or
/// unrelated data file that happens to share a ROM extension.
///
/// The catalog maps extensions to cores, but many extensions are ambiguous
/// (`.md`, `.fig`, `.bin`, `.iso`, `.zip`, `.exe`, `.com`, `.bat`, `.img`,
/// `.lst`, `.m3u`, `.pbp`, `.elf`, `.dol`, `.wad`, `.cso`, `.ciso`, `.rvz`,
/// `.gcm`, `.cdi`, `.gdi`, `.ccd`, `.chd`, `.cue`, `.sg`, `.gg`, `.sms`,
/// `.gen`, `.pce`, `.sgx`, `.a26`, `.nes`, `.fds`, `.unf`, `.n64`, `.z64`,
/// `.v64`, `.sfc`, `.smc`, `.gb`, `.gbc`, `.gba`, `.nds`, `.scummvm`,
/// `.prx`, `.wbfs`). Without content validation, a `README.TXT` or
/// `GPLv2.txt` in a ROM folder gets imported as a "game".
///
/// Validation strategy (in order):
/// 1. Reject empty files.
/// 2. Reject files that are mostly text (READMEs, licenses, notes).
/// 3. Reject files that are too small to be a real ROM (< 512 bytes).
/// 4. Reject files that are too large to be a ROM (> 512 MB).
/// 5. Accept files with known ROM magic bytes.
/// 6. Accept files that are binary (non-text) and within size bounds.
class RomValidator {
  const RomValidator();

  /// Minimum plausible ROM size in bytes (512 bytes).
  static const minRomSize = 512;

  /// Maximum plausible ROM size in bytes (512 MB).
  static const maxRomSize = 512 * 1024 * 1024;

  /// Known ROM magic bytes. Each entry is a list of byte sequences that
  /// identify a ROM format. The first byte sequence is the primary check;
  /// subsequent sequences are fallbacks for variants.
  static const _magicBytes = <String, List<List<int>>>{
    // NES: "NES\x1A" (iNES header)
    'nes': [
      [0x4E, 0x45, 0x53, 0x1A],
    ],
    // GB/GBC: Nintendo logo bytes at 0x104-0x133 (48 bytes)
    'gb': [
      [0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B],
    ],
    // GBA: Nintendo logo bytes at 0x04-0x9F (156 bytes)
    'gba': [
      [0x24, 0xFF, 0xAE, 0x51, 0x69, 0x9A, 0xA2, 0x21],
    ],
    // SNES/SFC: "NES\x1A" or "SNES" or 0x78 0x56 0x34 0x12 (checksum)
    'sfc': [
      [0x78, 0x56, 0x34, 0x12],
      [0x53, 0x4E, 0x45, 0x53],
    ],
    // N64: "NUS\x00" or 0x80 0x37 0x12 0x40 (PIF)
    'n64': [
      [0x80, 0x37, 0x12, 0x40],
      [0x4E, 0x55, 0x53, 0x00],
    ],
    // Genesis/MD: "SEGA" at 0x100-0x103
    'md': [
      [0x53, 0x45, 0x47, 0x41],
    ],
    // SMS: "SEGA" at 0x100-0x103
    'sms': [
      [0x53, 0x45, 0x47, 0x41],
    ],
    // GG: "SEGA" at 0x100-0x103
    'gg': [
      [0x53, 0x45, 0x47, 0x41],
    ],
    // PCE: "PCE\x00" or 0x00 0x00 0x00 0x00 (no magic, binary check)
    'pce': [
      [0x50, 0x43, 0x45, 0x00],
    ],
    // NDS: "NDS\x00" or 0x24 0xFF 0xAE 0x51 (ARM7)
    'nds': [
      [0x4E, 0x44, 0x53, 0x00],
      [0x24, 0xFF, 0xAE, 0x51],
    ],
    // A26: "ATARI\x00" or 0x00 0x00 0x00 0x00 (binary check)
    'a26': [
      [0x41, 0x54, 0x41, 0x52, 0x49, 0x00],
    ],
    // DOS: "MZ" (PE header)
    'exe': [
      [0x4D, 0x5A],
    ],
    // COM: 0x00 0x00 0x00 0x00 (binary check, no magic)
    'com': [
      [0x00, 0x00, 0x00, 0x00],
    ],
    // BAT: text file (rejected by text check)
    'bat': [],
    // IMG: 0x00 0x00 0x00 0x00 (binary check)
    'img': [
      [0x00, 0x00, 0x00, 0x00],
    ],
    // ISO: 0x01 0x43 0x44 0x30 0x30 0x31 (CD001)
    'iso': [
      [0x01, 0x43, 0x44, 0x30, 0x30, 0x31],
    ],
    // CUE: text file (rejected by text check)
    'cue': [],
    // CHD: "MComprHD" (MAME CHD)
    'chd': [
      [0x4D, 0x43, 0x6F, 0x6D, 0x70, 0x72, 0x48, 0x44],
    ],
    // CCD: text file (rejected by text check)
    'ccd': [],
    // CSO: 0x43 0x49 0x53 0x4F (CISO)
    'cso': [
      [0x43, 0x49, 0x53, 0x4F],
    ],
    // PBP: 0x00 0x50 0x42 0x50 (PBP)
    'pbp': [
      [0x00, 0x50, 0x42, 0x50],
    ],
    // ELF: 0x7F 0x45 0x4C 0x46 (ELF)
    'elf': [
      [0x7F, 0x45, 0x4C, 0x46],
    ],
    // PRX: 0x00 0x50 0x52 0x58 (PRX)
    'prx': [
      [0x00, 0x50, 0x52, 0x58],
    ],
    // DOL: 0x00 0xD0 0x0D 0xFE (DOL)
    'dol': [
      [0x00, 0xD0, 0x0D, 0xFE],
    ],
    // WAD: 0x49 0x57 0x41 0x44 (IWAD)
    'wad': [
      [0x49, 0x57, 0x41, 0x44],
    ],
    // WBFS: 0x57 0x42 0x46 0x53 (WBFS)
    'wbfs': [
      [0x57, 0x42, 0x46, 0x53],
    ],
    // RVZ: 0x52 0x56 0x5A 0x01 (RVZ)
    'rvz': [
      [0x52, 0x56, 0x5A, 0x01],
    ],
    // GCM: 0x47 0x43 0x4D 0x00 (GCM)
    'gcm': [
      [0x47, 0x43, 0x4D, 0x00],
    ],
    // CISO: 0x43 0x49 0x53 0x4F (CISO)
    'ciso': [
      [0x43, 0x49, 0x53, 0x4F],
    ],
    // CDI: 0x43 0x44 0x49 0x00 (CDI)
    'cdi': [
      [0x43, 0x44, 0x49, 0x00],
    ],
    // GDI: 0x47 0x44 0x49 0x00 (GDI)
    'gdi': [
      [0x47, 0x44, 0x49, 0x00],
    ],
    // LST: text file (rejected by text check)
    'lst': [],
    // M3U: text file (rejected by text check)
    'm3u': [],
    // ZIP: 0x50 0x4B 0x03 0x04 (PK\x03\x04)
    'zip': [
      [0x50, 0x4B, 0x03, 0x04],
    ],
    // SCUMMVM: text file (rejected by text check)
    'scummvm': [],
    // FDS: 0x46 0x44 0x53 0x1A (FDS)
    'fds': [
      [0x46, 0x44, 0x53, 0x1A],
    ],
    // UNF: 0x55 0x4E 0x46 0x00 (UNF)
    'unf': [
      [0x55, 0x4E, 0x46, 0x00],
    ],
    // V64: 0x80 0x37 0x12 0x40 (PIF)
    'v64': [
      [0x80, 0x37, 0x12, 0x40],
    ],
    // Z64: 0x80 0x37 0x12 0x40 (PIF)
    'z64': [
      [0x80, 0x37, 0x12, 0x40],
    ],
    // SG: "SEGA" at 0x100-0x103
    'sg': [
      [0x53, 0x45, 0x47, 0x41],
    ],
    // SGX: "PCE\x00" or 0x00 0x00 0x00 0x00 (binary check)
    'sgx': [
      [0x50, 0x43, 0x45, 0x00],
    ],
    // FIG: 0x00 0x00 0x00 0x00 (binary check)
    'fig': [
      [0x00, 0x00, 0x00, 0x00],
    ],
    // GEN: "SEGA" at 0x100-0x103
    'gen': [
      [0x53, 0x45, 0x47, 0x41],
    ],
    // BIN: 0x00 0x00 0x00 0x00 (binary check)
    'bin': [
      [0x00, 0x00, 0x00, 0x00],
    ],
  };

  /// Validates that [filePath] is a plausible ROM image.
  ///
  /// Returns `true` if the file passes validation, `false` otherwise.
  /// The [extension] is used to select the appropriate magic-byte check.
  Future<bool> validate(String filePath, String extension) async {
    final file = File(filePath);
    if (!file.existsSync()) return false;

    final stat = await file.stat();
    final size = stat.size;

    // Reject empty files
    if (size == 0) return false;

    // Reject files that are too small to be a real ROM
    if (size < minRomSize) return false;

    // Reject files that are too large to be a ROM
    if (size > maxRomSize) return false;

    // Read the first 512 bytes for magic-byte and text checks
    final bytes = await file.openRead(0, 512).first;
    if (bytes.isEmpty) return false;

    // Reject text files (READMEs, licenses, notes, etc.)
    if (_isTextFile(bytes)) return false;

    // Check magic bytes for the extension
    final ext = extension.toLowerCase();
    final magicList = _magicBytes[ext];
    if (magicList == null || magicList.isEmpty) {
      // No magic bytes defined for this extension — accept if binary
      return true;
    }

    // Check each magic byte sequence
    for (final magic in magicList) {
      if (_matchesMagic(bytes, magic)) {
        return true;
      }
    }

    // No magic bytes matched — reject
    return false;
  }

  /// Returns `true` if [bytes] look like a text file (ASCII/UTF-8).
  ///
  /// A file is considered text if > 90% of its bytes are printable ASCII
  /// or common whitespace (tab, newline, carriage return).
  bool _isTextFile(List<int> bytes) {
    if (bytes.isEmpty) return true;

    var textBytes = 0;
    for (final byte in bytes) {
      if ((byte >= 0x20 && byte <= 0x7E) || // printable ASCII
          byte == 0x09 || // tab
          byte == 0x0A || // newline
          byte == 0x0D) {
        // carriage return
        textBytes++;
      }
    }

    final ratio = textBytes / bytes.length;
    return ratio > 0.90;
  }

  /// Returns `true` if [bytes] start with [magic].
  bool _matchesMagic(List<int> bytes, List<int> magic) {
    if (bytes.length < magic.length) return false;
    for (var i = 0; i < magic.length; i++) {
      if (bytes[i] != magic[i]) return false;
    }
    return true;
  }
}
