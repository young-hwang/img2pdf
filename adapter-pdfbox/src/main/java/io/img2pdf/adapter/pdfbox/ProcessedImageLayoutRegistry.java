package io.img2pdf.adapter.pdfbox;

import java.nio.file.Path;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

final class ProcessedImageLayoutRegistry {
    private static final Map<Path, ProcessedImageLayout> LAYOUTS = new ConcurrentHashMap<>();

    private ProcessedImageLayoutRegistry() {
    }

    static void register(Path path, ProcessedImageLayout layout) {
        LAYOUTS.put(normalize(path), layout);
    }

    static ProcessedImageLayout lookup(Path path) {
        return LAYOUTS.get(normalize(path));
    }

    static void remove(Path path) {
        LAYOUTS.remove(normalize(path));
    }

    private static Path normalize(Path path) {
        return path.toAbsolutePath().normalize();
    }

    record ProcessedImageLayout(int originalWidth, int originalHeight, int offsetX, int offsetY) {
    }
}
