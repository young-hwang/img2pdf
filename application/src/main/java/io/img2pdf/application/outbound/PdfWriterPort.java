package io.img2pdf.application.outbound;

import io.img2pdf.domain.model.PdfOptions;

import java.nio.file.Path;
import java.util.List;

public interface PdfWriterPort {
    void write(List<Path> imagePaths, Path outputPdf, PdfOptions options);
}
