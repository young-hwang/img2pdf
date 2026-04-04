package io.img2pdf.application.dto;

import java.nio.file.Path;
import java.util.List;

public record ConvertImagesToPdfResult(
        Path outputPdf,
        List<Path> processedImages,
        String ocrText
) {
}
