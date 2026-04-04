package io.img2pdf.application.dto;

import io.img2pdf.domain.model.OcrOptions;
import io.img2pdf.domain.model.PdfOptions;

import java.nio.file.Path;
import java.util.List;

public record ConvertImagesToPdfRequest(
        List<Path> inputPaths,
        Path outputPdf,
        Path ocrTextOutput,
        PdfOptions pdfOptions,
        OcrOptions ocrOptions
) {
}
