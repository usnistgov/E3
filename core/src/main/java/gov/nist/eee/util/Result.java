package gov.nist.eee.util;

import java.util.function.Function;

public sealed interface Result<LEFT, RIGHT> permits Result.Success, Result.Failure {
    @SuppressWarnings("unchecked")
    default <T, T1 extends T> Result<T1, RIGHT> map(Function<LEFT, T1> mapper) {
        if(this instanceof Result.Success<LEFT, RIGHT> success)
            return new Success<>(mapper.apply(success.value));

        return (Result<T1, RIGHT>) this;
    }

    @SuppressWarnings("unchecked")
    default <T, T1 extends T, E> Result<T1, E> flatMap(Function<LEFT, Result<T1, E>> mapper) {
        if(this instanceof Result.Success<LEFT,RIGHT> success)
            return mapper.apply(success.value);

        return (Result<T1, E>) this;
    }

    record Success<T, E>(T value) implements Result<T, E> {
        @Override
        public <A> A on(Function<T, A> onSuccess, Function<E, A> onFailure) {
            return onSuccess.apply(value);
        }
    }

    record Failure<T, E>(E error) implements Result<T, E> {
        @Override
        public <A> A on(Function<T, A> onSuccess, Function<E, A> onFailure) {
            return onFailure.apply(error);
        }
    }

    <A> A on(Function<LEFT, A> onSuccess, Function<RIGHT, A> onFailure);
}