plugins {
    id("java")
}

group = "io.img2pdf"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

subprojects {
    tasks.withType<Jar>().configureEach {
        archiveBaseName = "img2pdf-${project.name}"
    }
}

tasks.test {
    useJUnitPlatform()
}
