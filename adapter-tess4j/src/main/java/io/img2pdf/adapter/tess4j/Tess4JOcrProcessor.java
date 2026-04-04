package io.img2pdf.adapter.tess4j;

import io.img2pdf.application.outbound.OcrProcessorPort;
import io.img2pdf.domain.model.OcrOptions;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;

import java.nio.file.Path;

public class Tess4JOcrProcessor implements OcrProcessorPort {

    @Override
    public String extractText(Path imagePath, OcrOptions options) {
        try {
            Tesseract tesseract = new Tesseract();

            if (options.tessdataPath() != null && !options.tessdataPath().isBlank()) {
                tesseract.setDatapath(options.tessdataPath());
            }

            if (options.language() != null && !options.language().isBlank()) {
                tesseract.setLanguage(options.language());
            }

            if (options.dpi() != null) {
                tesseract.setTessVariable("user_defined_dpi", String.valueOf(options.dpi()));
            }

            if (options.psm() != null) {
                tesseract.setPageSegMode(options.psm());
            }

            return tesseract.doOCR(imagePath.toFile());
        } catch (TesseractException e) {
            throw new IllegalStateException("OCR failed for: " + imagePath, e);
        }
    }
}
