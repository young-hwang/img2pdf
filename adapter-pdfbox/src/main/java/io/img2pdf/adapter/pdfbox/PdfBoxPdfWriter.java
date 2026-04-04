package io.img2pdf.adapter.pdfbox;

import io.img2pdf.application.outbound.PdfWriterPort;
import io.img2pdf.domain.model.PdfOptions;

import java.nio.file.Path;
import java.util.List;

public class PdfBoxPdfWriter implements PdfWriterPort {
    @Override
    public void write(List<Path> imagePaths, Path outputPdf, PdfOptions options) {

    }
}
