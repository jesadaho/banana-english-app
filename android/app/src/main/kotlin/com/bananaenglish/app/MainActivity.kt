package com.bananaenglish.app

import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.security.MessageDigest

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            "app.channel.shared.data",
        ).setMethodCallHandler { call, result ->
            when (call.method) {
                "openAppSettings" -> {
                    val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
                        data = Uri.fromParts("package", packageName, null)
                        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    }
                    startActivity(intent)
                    result.success(null)
                }

                // Required for Google API keys with Android app restrictions when
                // calling REST APIs via Dio (not Play Services client libraries).
                "getAndroidApiKeyAttestation" -> {
                    try {
                        result.success(
                            mapOf(
                                "packageName" to packageName,
                                "sha1" to signingCertSha1Hex(),
                            ),
                        )
                    } catch (e: Exception) {
                        result.error("ATTENTION", e.message, null)
                    }
                }

                else -> result.notImplemented()
            }
        }
    }

    private fun signingCertSha1Hex(): String {
        val signatures = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            val info = packageManager.getPackageInfo(
                packageName,
                PackageManager.GET_SIGNING_CERTIFICATES,
            )
            info.signingInfo?.apkContentsSigners ?: emptyArray()
        } else {
            @Suppress("DEPRECATION")
            val info = packageManager.getPackageInfo(
                packageName,
                PackageManager.GET_SIGNATURES,
            )
            @Suppress("DEPRECATION")
            info.signatures ?: emptyArray()
        }

        val signature = signatures.firstOrNull()
            ?: throw IllegalStateException("No signing certificate found")

        val digest = MessageDigest.getInstance("SHA-1").digest(signature.toByteArray())
        return digest.joinToString("") { "%02x".format(it) }
    }
}
