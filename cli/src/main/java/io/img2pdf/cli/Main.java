package io.img2pdf.cli;

import io.img2pdf.application.service.ConvertImagesToPdfService;
import picocli.CommandLine;

public class Main {
    static void main(String[] args) {

        var useCase = new ConvertImagesToPdfService();
        var command = new Scan2PdfCliCommand(useCase);
        int exitCode = new CommandLine(command).execute(args);
        System.exit(exitCode);
    }
}
