package io.img2pdf.domain.model;

public record OcrOptions(
        boolean enabled,
        String language,
        String tessdataPath,
        Integer dpi,
        Integer psm
) {

    public static OcrOptions disabled() {
        return new OcrOptions(false, "eng", null, null, null);
    }
}
