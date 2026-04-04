package io.img2pdf.adapter.pdfbox;

import io.img2pdf.application.outbound.PdfWriterPort;
import io.img2pdf.domain.model.PageSize;
import io.img2pdf.domain.model.PdfOptions;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.graphics.image.LosslessFactory;
import org.apache.pdfbox.pdmodel.graphics.image.PDImageXObject;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class PdfBoxPdfWriter implements PdfWriterPort {
    @Override
    public void write(List<Path> imagePaths, Path outputPdf, PdfOptions options) {
        try (PDDocument document = new PDDocument()) {
            for (Path imagePath : imagePaths) {
                BufferedImage image = ImageIO.read(imagePath.toFile());
                if (image == null) {
                    throw new IllegalArgumentException("Unsupported image file " + imagePath);
                }

                PDRectangle rectangle = resolvePageSize(options.pageSize(), image);
                PDPage page = new PDPage(rectangle);
                document.addPage(page);

                var pdImage = LosslessFactory.createFromImage(document, image);

                float pageWidth = rectangle.getWidth();
                float pageHeight = rectangle.getHeight();
                float imageWidth = image.getWidth();
                float imageHeight = image.getHeight();

                float drawWidth;
                float drawHeight;
                float x;
                float y;

                if (options.keepAspectRatio()) {
                    float widthScale = pageWidth / imageWidth;
                    float heightScale = pageHeight / imageHeight;
                    float scale = Math.min(widthScale, heightScale);

                    drawWidth = imageWidth * scale;
                    drawHeight = imageHeight * scale;
                    x = (pageWidth - drawWidth) / 2f;
                    y = (pageHeight - drawHeight) / 2f;
                } else {
                    drawWidth = pageWidth;
                    drawHeight = pageHeight;
                    x = 0;
                    y = 0;
                }

                try(PDPageContentStream contentStream = new PDPageContentStream(document, page)) {
                    contentStream.drawImage(pdImage, x, y, drawWidth, drawHeight);
                }
            }

            document.save(outputPdf.toFile());
        } catch (IOException e) {
            throw new IllegalStateException("Failed to create PDF: " + outputPdf, e);
        }
    }

    private PDRectangle resolvePageSize(PageSize pageSize, BufferedImage image) {
        return switch (pageSize) {
            case A4 -> PDRectangle.A4;
            case A5 -> PDRectangle.A5;
            case LETTER -> PDRectangle.LETTER;
            case ORIGINAL -> new PDRectangle(image.getWidth(), image.getHeight());
        };
    }
}
