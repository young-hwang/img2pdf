package io.img2pdf.application.service;

import io.img2pdf.application.dto.ConvertImagesToPdfRequest;
import io.img2pdf.application.dto.ConvertImagesToPdfResult;
import io.img2pdf.application.inbound.ConvertImagesToPdfUseCase;
import io.img2pdf.application.outbound.OcrProcessorPort;
import io.img2pdf.application.outbound.PdfWriterPort;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
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

        String ocrText = "";
        if (request.ocrOptions().enabled()) {
            StringBuilder sb = new StringBuilder();

            for (Path imageFile : imageFiles) {
                String text = ocrProcessorPort.extractText(imageFile, request.ocrOptions());
                sb.append("===== ")
                        .append(imageFile.getFileName())
                        .append(" =====")
                        .append(System.lineSeparator())
                        .append(text)
                        .append(System.lineSeparator())
                        .append(System.lineSeparator());
            }

            ocrText = sb.toString();

            if (request.ocrTextOutput() != null) {
                writeTextFile(request.ocrTextOutput(), ocrText);
            }
        }
        return new ConvertImagesToPdfResult(
                request.outputPdf(),
                imageFiles,
                ocrText
        );
    }

    private void writeTextFile(Path output, String text) {
        try {
            createParentDirectoryIfNeeded(output);
            Files.writeString(output, text, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException("Failed to write OCR text file: " + output, e);
        }
    }

    private void createParentDirectoryIfNeeded(Path file) {
        try {
            Path parent = file.toAbsolutePath().getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
        } catch (IOException e) {
            throw new IllegalStateException("Failed to create parent directory for: " + file, e);
        }
    }
}
