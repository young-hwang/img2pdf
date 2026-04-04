package io.img2pdf.application.service;

import io.img2pdf.application.dto.ConvertImagesToPdfRequest;
import io.img2pdf.application.dto.ConvertImagesToPdfResult;
import io.img2pdf.application.inbound.ConvertImagesToPdfUseCase;
import io.img2pdf.application.outbound.OcrProcessorPort;
import io.img2pdf.application.outbound.PdfWriterPort;

import java.nio.file.Path;
import java.util.List;

public class ConvertImagesToPdfService implements ConvertImagesToPdfUseCase {

    private final OcrProcessorPort ocrProcessorPort;
    private final PdfWriterPort pdfWriterPort;
    private final FileCollector fileCollector;

    public ConvertImagesToPdfService(OcrProcessorPort ocrProcessorPort, PdfWriterPort pdfWriterPort, FileCollector fileCollector) {
        this.ocrProcessorPort = ocrProcessorPort;
        this.pdfWriterPort = pdfWriterPort;
        this.fileCollector = fileCollector;
    }

    @Override
    public ConvertImagesToPdfResult handle(ConvertImagesToPdfRequest request) {
        List<Path> imageFiles = fileCollector.collectImages(request.inputPaths());

        if (imageFiles.isEmpty()) {
            throw new IllegalArgumentException("No supported image files found.");
        }

        createParentDirectoryIfNeeded(request.outputPdf());
        pdfWriterPort.write(imageFiles, request.outputPdf(), request.pdfOptions());

        return null;
    }

    private void createParentDirectoryIfNeeded(Path path) {

    }
}
