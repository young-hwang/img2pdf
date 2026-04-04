package io.img2pdf.application.outbound;

import io.img2pdf.domain.model.OcrOptions;

import java.nio.file.Path;

public interface OcrProcessorPort {
    String extractText(Path imagePath, OcrOptions options);
}
