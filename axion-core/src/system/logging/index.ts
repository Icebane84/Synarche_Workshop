/**
 * src/system/logging/ — Nexus Beacon & TypeScript Logger Bridge
 * =============================================================
 * Python modules: phoenix_logger.py
 *
 * [OMNI-ARTIFACT-ANCHOR] ID: SYSTEM.LOGGING.Gateway VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-28
 */

import * as fs from "fs";
import * as path from "path";

/**
 * Standardized process status levels.
 */
export enum ProcessStatus {
    INFO = "INFO",
    WARNING = "WARNING",
    ERROR = "ERROR",
    CRITICAL = "CRITICAL",
    DEBUG = "DEBUG",
    TRACE = "TRACE"
}

/**
 * TypeScript implementation of the PhoenixLogger.
 * Aligns with UMB-PHX-LOG-001 by implementing dual-stream behavior:
 * 1. stdout (Console) for real-time transparency (INFO and above).
 * 2. error_audit.log for persistent accountability (ERROR and above).
 */
export class PhoenixLogger {
    private static logFilePath = path.resolve(process.cwd(), "error_audit.log");

    public static info(message: string, ...optionalParams: any[]): void {
        this.log(ProcessStatus.INFO, message, optionalParams);
    }

    public static warning(message: string, ...optionalParams: any[]): void {
        this.log(ProcessStatus.WARNING, message, optionalParams);
    }

    public static error(message: string, ...optionalParams: any[]): void {
        this.log(ProcessStatus.ERROR, message, optionalParams);
    }

    public static critical(message: string, ...optionalParams: any[]): void {
        this.log(ProcessStatus.CRITICAL, message, optionalParams);
    }

    public static debug(message: string, ...optionalParams: any[]): void {
        this.log(ProcessStatus.DEBUG, message, optionalParams);
    }

    public static trace(message: string, ...optionalParams: any[]): void {
        this.log(ProcessStatus.TRACE, message, optionalParams);
    }

    /**
     * Formats and logs the message as per the Phoenix Logging Protocol.
     */
    private static log(level: ProcessStatus, message: string, params: any[]): void {
        const timestamp = new Date().toISOString().replace("T", " ").substring(0, 19);
        const paramStr = params && params.length > 0 ? " " + params.map(p => typeof p === "object" ? JSON.stringify(p) : String(p)).join(" ") : "";
        const formattedMessage = `${timestamp} - PhoenixLogger - ${level} - ${message}${paramStr}`;

        // 1. Console (INFO and above)
        if (level !== ProcessStatus.DEBUG && level !== ProcessStatus.TRACE) {
            if (level === ProcessStatus.ERROR || level === ProcessStatus.CRITICAL) {
                console.error(formattedMessage);
            } else {
                console.log(formattedMessage);
            }
        }

        // 2. Persistent file log (ERROR and above)
        if (level === ProcessStatus.ERROR || level === ProcessStatus.CRITICAL) {
            try {
                fs.appendFileSync(this.logFilePath, formattedMessage + "\n", "utf8");
            } catch (err) {
                console.warn(`Failed to write to error_audit.log: ${err}`);
            }
        }
    }
}
