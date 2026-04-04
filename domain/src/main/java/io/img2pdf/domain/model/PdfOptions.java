package io.img2pdf.domain.model;

public record PdfOptions(
    PageSize pageSize,
    boolean keepAspectRatio) {
}
