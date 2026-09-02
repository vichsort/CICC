import { onMounted, onUnmounted } from 'vue';

/**
 * Composable para gerenciar inatividade do usuário em quiosques/totens.
 * Executa uma ação (callback) se nenhum toque, clique ou tecla for detectado após timeoutMs.
 *
 * @param {Function} onTimeout Callback executado quando o tempo de inatividade expira.
 * @param {number} timeoutMs Tempo em milissegundos (padrão: 60000ms = 60s).
 * @param {import('vue').Ref<boolean>} [isPausedRef] Ref opcional que pausa o timer quando true.
 */
export function useInactivityTimeout(onTimeout, timeoutMs = 60000, isPausedRef = null) {
  let timer = null;

  const activityEvents = ['touchstart', 'pointerdown', 'mousedown', 'keydown'];

  function resetTimer() {
    if (timer) {
      clearTimeout(timer);
    }

    if (isPausedRef && isPausedRef.value) {
      return;
    }

    timer = setTimeout(() => {
      onTimeout();
    }, timeoutMs);
  }

  function stopTimer() {
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
  }

  onMounted(() => {
    activityEvents.forEach(evt => {
      window.addEventListener(evt, resetTimer, { passive: true });
    });
    resetTimer();
  });

  onUnmounted(() => {
    stopTimer();
    activityEvents.forEach(evt => {
      window.removeEventListener(evt, resetTimer);
    });
  });

  return {
    resetTimer,
    stopTimer
  };
}

