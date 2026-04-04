package io.img2pdf.application.inbound;

import io.img2pdf.application.dto.ConvertImagesToPdfRequest;
import io.img2pdf.application.dto.ConvertImagesToPdfResult;

public interface ConvertImagesToPdfUseCase {
    ConvertImagesToPdfResult handle(ConvertImagesToPdfRequest request);
}
